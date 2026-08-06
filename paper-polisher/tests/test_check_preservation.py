from __future__ import annotations

import contextlib
import importlib.util
import io
import subprocess
import sys
import tempfile
import unittest
from collections.abc import Callable
from pathlib import Path


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "check_preservation.py"
SPEC = importlib.util.spec_from_file_location("paper_polisher_check_preservation", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
CHECKER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECKER
SPEC.loader.exec_module(CHECKER)


class MathPreservationTests(unittest.TestCase):
    def check(self, original: str, polished: str, *, allow_additions: bool = False) -> tuple[bool, str]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            passed = CHECKER.check_math_preservation(
                original, polished, limit=20, allow_additions=allow_additions
            )
        return passed, output.getvalue()

    def assert_math_passes(
        self, original: str, polished: str, *, allow_additions: bool = False
    ) -> None:
        passed, output = self.check(original, polished, allow_additions=allow_additions)
        self.assertTrue(passed, output)

    def assert_math_fails(
        self, original: str, polished: str, *, allow_additions: bool = False
    ) -> None:
        passed, output = self.check(original, polished, allow_additions=allow_additions)
        self.assertFalse(passed, output)

    def test_ignores_math_whitespace_and_comments(self) -> None:
        original = r"\[M+x\]"
        polished = "\\[\n  M % layout note\n  +   x\n\\]"
        self.assert_math_passes(original, polished)

    def test_preserves_normalized_whitespace_inside_math_text(self) -> None:
        self.assert_math_passes(r"$\text{not equal}$", r"$\text{not   equal}$")
        self.assert_math_fails(r"$\text{not equal}$", r"$\text{note qual}$")
        self.assert_math_fails(r"$\textsc{not equal}$", r"$\textsc{note qual}$")
        self.assert_math_fails(r"$\textmd{not equal}$", r"$\textmd{note qual}$")

    def test_tex_comments_join_lines_without_inventing_text_space(self) -> None:
        original = "$\\text{not% comment\n  equal}$"
        self.assert_math_passes(original, r"$\text{notequal}$")
        self.assert_math_fails(original, r"$\text{not equal}$")

    def test_ignores_layout_whitespace_in_math_nested_inside_text(self) -> None:
        self.assert_math_passes(
            r"\[\text{value $x+y$}\]",
            r"\[\text{value $x + y$}\]",
        )
        self.assert_math_passes(
            r"\[\text{value \(x+y\)}\]",
            r"\[\text{value \(x + y\)}\]",
        )
        self.assert_math_passes(
            r"\[\text{value \ensuremath{x+y}}\]",
            r"\[\text{value \ensuremath{x + y}}\]",
        )

    def test_detects_variable_changes_for_all_supported_delimiters(self) -> None:
        pairs = [
            (r"$M$", r"$N$"),
            (r"$$M$$", r"$$N$$"),
            (r"\(M\)", r"\(N\)"),
            (r"\[M\]", r"\[N\]"),
            (
                r"\begin{equation}M\end{equation}",
                r"\begin{equation}N\end{equation}",
            ),
        ]
        for original, polished in pairs:
            with self.subTest(original=original):
                self.assert_math_fails(original, polished)
                self.assert_math_fails(original, polished, allow_additions=True)

    def test_detects_changes_in_standalone_ensuremath(self) -> None:
        self.assert_math_fails(r"State \ensuremath{M}.", r"State \ensuremath{N}.")
        self.assert_math_fails(
            r"State \ensuremath{M}.",
            r"State \ensuremath{N}.",
            allow_additions=True,
        )

    def test_detects_change_inside_nested_math_environment(self) -> None:
        original = r"\begin{equation}\begin{aligned}y&=Mx\end{aligned}\end{equation}"
        polished = r"\begin{equation}\begin{aligned}y&=Nx\end{aligned}\end{equation}"
        self.assert_math_fails(original, polished)

    def test_detects_changes_in_additional_amsmath_environments(self) -> None:
        original = r"\begin{xalignat}{2}a&=b\end{xalignat}"
        polished = r"\begin{xalignat}{2}a&=c\end{xalignat}"
        self.assert_math_fails(original, polished)

    def test_detects_math_changes_inside_diagram_environments(self) -> None:
        original = r"\begin{tikzpicture}\node {$M$};\end{tikzpicture}"
        polished = r"\begin{tikzpicture}\node {$N$};\end{tikzpicture}"
        self.assert_math_fails(original, polished)

    def test_requires_math_delimiter_and_environment_kind_preservation(self) -> None:
        self.assert_math_fails(r"$M$", r"\(M\)")
        self.assert_math_fails(
            r"\begin{align}M&=N\end{align}",
            r"\begin{align*}M&=N\end{align*}",
        )

    def test_all_modes_reject_new_math_region(self) -> None:
        original = r"The state is $x$."
        polished = r"The state is $x$, and the input is $u$."
        self.assert_math_fails(original, polished)
        self.assert_math_fails(original, polished, allow_additions=True)

    def test_additions_mode_rejects_repeated_region_with_middle_insertion(self) -> None:
        original = r"First $x$. Second $x$. Third $x$."
        polished = r"First $x$. New $y$. Second $x$. Third $x$."
        self.assert_math_fails(original, polished, allow_additions=True)

    def test_additions_mode_rejects_edits_inside_existing_math_region(self) -> None:
        original = r"\[y=Mx\]"
        inserted = r"\[y=Mx+b\]"
        replaced = r"\[y=Nx+b\]"
        self.assert_math_fails(original, inserted)
        self.assert_math_fails(original, inserted, allow_additions=True)
        self.assert_math_fails(original, replaced, allow_additions=True)

        for changed_symbol in (r"$x_i$", r"$M^{-1}$"):
            with self.subTest(changed_symbol=changed_symbol):
                source = r"$x$" if "x" in changed_symbol else r"$M$"
                self.assert_math_fails(source, changed_symbol, allow_additions=True)

    def test_additions_mode_rejects_deleted_tokens(self) -> None:
        original = r"\[y=Mx+b\]"
        polished = r"\[y=Mx\]"
        self.assert_math_fails(original, polished)
        self.assert_math_fails(original, polished, allow_additions=True)

    def test_duplicate_regions_are_matched_one_to_one(self) -> None:
        original = r"First $M$. Second $M$."
        polished = r"Only $M$."
        self.assert_math_fails(original, polished)
        self.assert_math_fails(original, polished, allow_additions=True)

    def test_region_reordering_is_reported(self) -> None:
        original = r"First $M$. Second $N$."
        polished = r"Second $N$. First $M$."
        self.assert_math_fails(original, polished)
        self.assert_math_fails(original, polished, allow_additions=True)

    def test_malformed_math_fails_without_false_pass(self) -> None:
        passed, output = self.check(r"Text $M", r"Text $M")
        self.assertFalse(passed)
        self.assertIn("unclosed inline-math delimiter", output)

        passed, output = self.check(
            r"\begin{equation}M", r"\begin{equation}M"
        )
        self.assertFalse(passed)
        self.assertIn("unclosed math environment", output)

    def test_ignores_math_like_text_in_comments_and_literal_commands(self) -> None:
        original = "% $M$\n" + r"\verb|$M$| Actual $x$."
        polished = "% $N$\n" + r"\verb|$N$| Actual $x$."
        self.assert_math_passes(original, polished)

    def test_ignores_dollars_in_opaque_command_arguments(self) -> None:
        source = r"\url{https://example.com/$id} and \path{results/$run} with state $x$."
        self.assert_math_passes(source, source)

    def test_percent_in_verbatim_like_url_does_not_hide_following_math(self) -> None:
        original = r"\url{https://example.com/a%20b} with state $x$."
        polished = r"\url{https://example.com/a%20b} with state $y$."
        self.assert_math_fails(original, polished)

    def test_percent_in_url_does_not_hide_following_checks(self) -> None:
        source = r"\url{https://example.com/a%20b} Bad -- prose. \label{sec:test}"
        self.assertTrue(CHECKER.collect_prohibited_dashes(source))
        keys = CHECKER.collect_structural_keys(source)
        self.assertEqual(keys["label"]["sec:test"], 1)

    def test_compares_opaque_math_arguments_without_mode_switching(self) -> None:
        original = r"$\text{see \url{foo/$id} not equal}$"
        changed_text = r"$\text{see \url{foo/$id} note qual}$"
        changed_url = r"$\text{see \url{foo/$run} not equal}$"
        self.assert_math_fails(original, changed_text)
        self.assert_math_fails(original, changed_url)

    def test_still_checks_visible_href_text(self) -> None:
        original = r"\href{https://example.com/$id}{$x$}"
        polished = r"\href{https://example.com/$id}{$y$}"
        self.assert_math_fails(original, polished)

    def test_math_label_binding_is_preserved(self) -> None:
        original = r"\begin{equation}M\label{eq:model}\end{equation}"
        polished = r"\begin{equation}N\label{eq:model}\end{equation}"
        self.assert_math_fails(original, polished)


class EndToEndPreservationContractTests(unittest.TestCase):
    def run_pair(
        self,
        original: str,
        polished: str,
        *extra_args: str,
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            original_path = root / "original.tex"
            polished_path = root / "polished.tex"
            original_path.write_text(original, encoding="utf-8")
            polished_path.write_text(polished, encoding="utf-8")
            return subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    str(original_path),
                    str(polished_path),
                    *extra_args,
                ],
                capture_output=True,
                text=True,
                check=False,
            )

    def assert_pair_passes(
        self,
        original: str,
        polished: str,
        *extra_args: str,
    ) -> None:
        result = self.run_pair(original, polished, *extra_args)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def assert_pair_fails(
        self,
        original: str,
        polished: str,
        *extra_args: str,
    ) -> None:
        result = self.run_pair(original, polished, *extra_args)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def assert_rejected_in_all_modes(self, original: str, polished: str) -> None:
        for extra_args in ((), ("--allow-additions",)):
            with self.subTest(extra_args=extra_args):
                self.assert_pair_fails(original, polished, *extra_args)

    def test_numeric_tokens_are_hard_protected_in_all_modes(self) -> None:
        mutations = {
            "value": ("Latency is 12 ms.", "Latency is 13 ms."),
            "unit": ("Latency is 12 ms.", "Latency is 12 s."),
            "sign": ("The gain is +12 dB.", "The gain is -12 dB."),
            "unicode_minus_sign": ("The gain is −3.2 dB.", "The gain is 3.2 dB."),
            "order": (
                "Stage A takes 1 ms and stage B takes 2 ms.",
                "Stage A takes 2 ms and stage B takes 1 ms.",
            ),
            "addition": ("Latency is 12 ms.", "Latency is 12 ms with 3 trials."),
            "deletion": ("Latency is 12 ms with 3 trials.", "Latency is 12 ms."),
        }
        for mutation, (original, polished) in mutations.items():
            with self.subTest(mutation=mutation):
                self.assert_rejected_in_all_modes(original, polished)

    def test_numeric_scanner_protects_units_detached_signs_and_embedded_digits(self) -> None:
        mutations = {
            "SI force unit": ("The load is 10 N.", "The load is 10 kN."),
            "custom word unit": ("The length is 10 furlongs.", "The length is 10 parsecs."),
            "compound unit": ("Density is 10 kg/m^3.", "Density is 10 kg/cm^3."),
            "spaced compound unit": ("Density is 10 kg m⁻³.", "Density is 10 kg cm⁻³."),
            "pressure unit": ("Pressure is 10 psi.", "Pressure is 10 bar."),
            "inch abbreviation": ("Length is 10 in.", "Length is 10."),
            "rotation unit": ("Speed is 10 rpm.", "Speed is 10 rps."),
            "square unit symbol": ("Mass is 10 ㎏.", "Mass is 10 ㎎."),
            "detached sign": ("The deviation is ± 0.3 %.", "The deviation is + 0.3 %."),
            "narrow-space sign": ("The deviation is ± 0.3 %.", "The deviation is 0.3 %."),
            "thin-space sign": ("The deviation is ± 0.3 %.", "The deviation is + 0.3 %."),
            "newline sign": ("The deviation is ±\n0.3 %.", "The deviation is +\n0.3 %."),
            "minus-or-plus sign": ("The deviation is ∓12 %.", "The deviation is 12 %."),
            "superscript sign": ("Scale is 10⁻³.", "Scale is 10³."),
            "subscript sign": ("Exponent ₋₃ applies.", "Exponent ₊₃ applies."),
            "TeX-spaced fraction sign": (r"Use ±\,½.", r"Use \,½."),
            "TeX control-space sign": (
                r"The deviation is ±\ 0.3 %.",
                r"The deviation is +\ 0.3 %.",
            ),
            "TeX quad-spaced sign": (
                r"The deviation is ±\quad 0.3 %.",
                r"The deviation is +\quad 0.3 %.",
            ),
            "TeX hspace unit": (
                r"Latency is 10\hspace{1pt}ms.",
                r"Latency is 10\hspace{1pt}s.",
            ),
            "TeX hspace sign": (
                r"The deviation is ±\hspace{1pt}3 dB.",
                r"The deviation is +\hspace{1pt}3 dB.",
            ),
            "TeX hspace magnitude": (
                r"Latency is 10\hspace{1pt}ms.",
                r"Latency is 10\hspace{2pt}ms.",
            ),
            "TeX negative thin-space unit": (
                r"Latency is 10\negthinspace ms.",
                r"Latency is 10\negthinspace s.",
            ),
            "TeX enskip sign": (
                r"The deviation is ±\enskip 0.3 %.",
                r"The deviation is +\enskip 0.3 %.",
            ),
            "TeX kern unit": (
                r"Latency is 10\kern1pt ms.",
                r"Latency is 10\kern1pt s.",
            ),
            "TeX hskip currency": (
                r"Budget is USD\hskip 1pt 10.",
                r"Budget is EUR\hskip 1pt 10.",
            ),
            "TeX mspace unit": (
                r"Latency is 10\mspace{3mu}ms.",
                r"Latency is 10\mspace{3mu}s.",
            ),
            "nested TeX hspace unit": (
                r"Latency is 10\hspace{\widthof{M}}ms.",
                r"Latency is 10\hspace{\widthof{M}}s.",
            ),
            "empty group unit": (
                r"Latency is 10{}ms.",
                r"Latency is 10{}s.",
            ),
            "empty group sign": (
                r"The deviation is ±{}0.3 %.",
                r"The deviation is +{}0.3 %.",
            ),
            "empty group currency": (
                r"Budget is USD{}10.",
                r"Budget is EUR{}10.",
            ),
            "empty group marker": (
                r"Accuracy is 91.2{}*.",
                r"Accuracy is 91.2{}†.",
            ),
            "grouped spacing unit": (
                r"Latency is 10{\hspace{1pt}}ms.",
                r"Latency is 10{\hspace{1pt}}s.",
            ),
            "nested empty group unit": (
                r"Latency is 10{{}}ms.",
                r"Latency is 10{{}}s.",
            ),
            "nested empty group sign": (
                r"The deviation is ±{{}}0.3 %.",
                r"The deviation is +{{}}0.3 %.",
            ),
            "nested group after literal anchor": (
                r"Value \verb|10|{{}}ms.",
                r"Value \verb|10|{{}}s.",
            ),
            "comment-spliced unit": (
                "Latency is 10% join\nms.",
                "Latency is 10% join\ns.",
            ),
            "comment-spliced sign": (
                "The deviation is ±% join\n3 dB.",
                "The deviation is +% join\n3 dB.",
            ),
            "comment-spliced marker": (
                "Accuracy is 91.2% join\n*.",
                "Accuracy is 91.2% join\n†.",
            ),
            "textual-number sign": (
                "The deviation is ± ten percent.",
                "The deviation is + ten percent.",
            ),
            "textual-number currency": (
                "Budget is USD ten.",
                "Budget is EUR ten.",
            ),
            "textual-number comment marker": (
                "Accuracy is ten% join\n*.",
                "Accuracy is ten% join\n†.",
            ),
            "attached uncertainty sign": (
                "Accuracy is 91.2±0.3%.",
                "Accuracy is 91.2+0.3%.",
            ),
            "attached minus-or-plus sign": (
                "Accuracy is 91.2∓0.3%.",
                "Accuracy is 91.2±0.3%.",
            ),
            "embedded digit": ("The system uses IPv4.", "The system uses IPv6."),
            "superscript digit": ("Area is 10 m².", "Area is 10 m³."),
            "vulgar fraction": ("Use ½ of the set.", "Use ⅓ of the set."),
            "circled digit": ("Case ① applies.", "Case ② applies."),
            "fullwidth punctuation": ("Score is １２．５ %.", "Score is １２，５ %."),
            "textual number": ("We ran ten trials.", "We ran eleven trials."),
            "contextual Roman number": ("Type II applies.", "Type I applies."),
            "significance star": ("Accuracy is 91.2*.", "Accuracy is 91.2."),
            "significance dagger": ("Accuracy is 91.2†.", "Accuracy is 91.2."),
            "spaced significance marker": ("Accuracy is 91.2 †.", "Accuracy is 91.2."),
            "TeX superscript marker": (
                r"Accuracy is 91.2\textsuperscript{*}.",
                r"Accuracy is 91.2\textsuperscript{†}.",
            ),
            "currency prefix": ("Cost is USD 10.", "Cost is EUR 10."),
            "currency prefix with TeX nonbreaking space": (
                "Cost is USD~10.",
                "Cost is EUR~10.",
            ),
            "unit after dollar math": (
                r"Latency is $10$ ms.",
                r"Latency is $10$ s.",
            ),
            "unit after parenthesized math": (
                r"Latency is \(10\) ms.",
                r"Latency is \(10\) s.",
            ),
            "currency after math": (
                r"Budget is $10$ USD.",
                r"Budget is $10$ EUR.",
            ),
            "sign before math": (
                "The deviation is ±$3$ dB.",
                "The deviation is +$3$ dB.",
            ),
            "sign before numeric macro": (
                r"The deviation is ±\num{3} dB.",
                r"The deviation is +\num{3} dB.",
            ),
            "marker after parenthesized math": (
                "Accuracy is \\(91.2\\)†.",
                "Accuracy is \\(91.2\\)‡.",
            ),
            "marker after math percent": (
                "Accuracy is $91.2\\%$†.",
                "Accuracy is $91.2\\%$‡.",
            ),
            "marker after numeric macro": (
                r"Accuracy is \num{91.2}\textsuperscript{*}.",
                r"Accuracy is \num{91.2}\textsuperscript{a}.",
            ),
            "time word unit": (
                "Training took 10 weeks.",
                "Training took 10 years.",
            ),
            "spaced mechanical compound unit": (
                "Torque is 10 N m.",
                "Torque is 10 N s.",
            ),
            "spaced pressure-time compound unit": (
                "Exposure is 10 Pa s.",
                "Exposure is 10 Pa m.",
            ),
            "TeX-spaced compound unit": (
                r"Torque is 10 N\,m.",
                r"Torque is 10 N\,s.",
            ),
            "attached compound unit": (
                "Torque is 10Nm.",
                "Torque is 10Ns.",
            ),
            "experiment count unit": (
                "Training used 10 epochs.",
                "Training used 10 iterations.",
            ),
            "sample count unit": (
                "We used 10 samples.",
                "We used 10 trials.",
            ),
            "fold number word": (
                "The speedup is twofold.",
                "The speedup is threefold.",
            ),
            "quantitative adjective": (
                "A single run was used.",
                "A double run was used.",
            ),
            "quantifier": (
                "Both runs converged.",
                "Either run converged.",
            ),
            "extended currency prefix": ("Cost is NZD 10.", "Cost is SEK 10."),
            "currency suffix": ("Cost is 10 €.", "Cost is 10 £."),
            "literal digit": (r"Use \verb|version 2|.", r"Use \verb|version 3|."),
            "literal numeric anchor unit": (
                r"Value \verb|10| ms.",
                r"Value \verb|10| s.",
            ),
            "literal numeric anchor marker": (
                r"Value \verb|91.2|*.",
                r"Value \verb|91.2|†.",
            ),
            "text command numeric anchor": (
                r"Value \texttt{10} ms.",
                r"Value \texttt{10} s.",
            ),
            "standalone parenthesized unit": (
                "Latency (ms) is reported.",
                "Latency (s) is reported.",
            ),
            "standalone bracketed unit": (
                "Latency [ms] is reported.",
                "Latency [s] is reported.",
            ),
            "standalone currency": (
                "Budget (USD) is reported.",
                "Budget (EUR) is reported.",
            ),
            "standalone sign": (
                "Positive class (+) is used.",
                "Positive class (-) is used.",
            ),
            "unit cue": (
                "Latency is measured in milliseconds.",
                "Latency is measured in seconds.",
            ),
            "currency cue": (
                "The currency is USD.",
                "The currency is EUR.",
            ),
            "sign cue": (
                "Uncertainty is denoted by ±.",
                "Uncertainty is denoted by +.",
            ),
            "marker cue": (
                "Significance: * means p < 0.05.",
                "Significance: † means p < 0.05.",
            ),
            "denoted marker cue": (
                "Significance is denoted by *.",
                "Significance is denoted by †.",
            ),
            "marker before math anchor": (
                "* $p<0.05$ is significant.",
                "† $p<0.05$ is significant.",
            ),
            "comment digit": ("% run 2\nText.", "% run 3\nText."),
        }
        for mutation, (original, polished) in mutations.items():
            with self.subTest(mutation=mutation):
                self.assert_rejected_in_all_modes(original, polished)

    def test_quantity_scanner_does_not_freeze_ordinary_following_prose(self) -> None:
        self.assert_pair_passes(
            "Experiment 2 presents results.",
            "Experiment 2 shows results.",
        )
        self.assert_pair_passes(
            "We tested 10 different models.",
            "We tested 10 distinct models.",
        )
        self.assert_pair_passes(
            "One can observe this trend.",
            "We can observe this trend.",
        )
        self.assert_pair_passes(
            "Thus, one can observe this trend.",
            "Thus, we can observe this trend.",
        )
        self.assert_pair_passes(
            "One cannot infer causality.",
            "Causality cannot be inferred.",
        )
        self.assert_pair_passes(
            "One often observes this trend.",
            "This trend is often observed.",
        )
        self.assert_pair_passes(
            "Thus, one observes this trend.",
            "Thus, we observe this trend.",
        )
        self.assert_pair_passes(
            "One does not imply the other.",
            "Neither implies the other.",
        )
        self.assert_pair_passes(
            "One is able to derive the bound.",
            "The bound can be derived.",
        )
        self.assert_pair_passes(
            "One is tempted to infer causality.",
            "It is tempting to infer causality.",
        )
        self.assert_pair_passes(
            "The variables interact with one another.",
            "The variables interact with each other.",
        )
        self.assert_pair_passes(
            "We used 10 in our study.",
            "In our study, we used 10.",
        )
        self.assert_pair_passes(
            "We ran ABC 10 times.",
            "Using ABC, we ran 10 times.",
        )
        self.assert_pair_passes(
            "At step 10 CNN is evaluated.",
            "CNN is evaluated at step 10.",
        )
        self.assert_pair_passes(
            "% run 10\nCNN works.",
            "% run 10\nThe CNN works.",
        )
        self.assert_pair_passes(
            "We second this recommendation.",
            "We support this recommendation.",
        )
        self.assert_pair_passes(
            "We second the recommendation.",
            "We support the recommendation.",
        )
        self.assert_pair_passes(
            "We pair each input with its target.",
            "We match each input with its target.",
        )
        self.assert_pair_passes(
            "We pair observations across views.",
            "We match observations across views.",
        )
        self.assert_pair_passes(
            "We single out the difficult cases.",
            "We isolate the difficult cases.",
        )
        self.assert_pair_passes(
            "We single difficult cases out.",
            "We isolate difficult cases.",
        )
        self.assert_pair_passes(
            "We second Smith's recommendation.",
            "We support Smith's recommendation.",
        )
        self.assert_pair_passes(
            "We trained 10 A samples.",
            "We trained 10 samples from class A.",
        )
        self.assert_pair_passes(
            "Experiment 2 runs efficiently.",
            "Experiment 2 executes efficiently.",
        )
        self.assert_pair_passes(
            "Model 2 samples the stream.",
            "Model 2 draws from the stream.",
        )
        self.assert_pair_passes(
            r"Version \verb|v2| runs correctly.",
            r"Version \verb|v2| executes correctly.",
        )
        self.assert_pair_passes(
            r"Version \texttt{2} runs correctly.",
            r"Version \texttt{2} executes correctly.",
        )
        self.assert_pair_passes(
            "Use sample(s) when the count is unknown.",
            "Use samples when the count is unknown.",
        )
        self.assert_pair_passes(
            "We used configuration 10 in long runs.",
            "In long runs, we used configuration 10.",
        )

    def test_pronominal_one_heuristic_keeps_quantitative_one_protected(self) -> None:
        self.assert_rejected_in_all_modes(
            "One model converged.",
            "Two models converged.",
        )

    def test_dash_free_range_rewrite_preserves_unsigned_values(self) -> None:
        self.assert_pair_passes(
            "The range is 1--2 m.",
            "The range is from 1 to 2 m.",
        )

    def test_terminal_decimal_punctuation_can_move_without_changing_number(self) -> None:
        original = "The final count is 10."
        polished = "At count 10, the evaluation ends."
        self.assert_pair_passes(original, polished)
        self.assert_pair_passes(original, polished, "--allow-additions")

    def test_allow_additions_does_not_relax_protected_content(self) -> None:
        protected_mutations = {
            "math": (r"State $x$.", r"State $x$ and input $u$."),
            "structure": (
                r"\section{Method}\label{sec:method}Text.",
                r"\section{Method}\label{sec:method}Text."
                r"\section{Extra}\label{sec:extra}More text.",
            ),
            "number": ("There are 4 cases.", "There are 4 cases and 2 variants."),
        }
        for protected_kind, (original, polished) in protected_mutations.items():
            with self.subTest(protected_kind=protected_kind):
                self.assert_pair_fails(original, polished, "--allow-additions")

    def test_replacing_math_symbol_then_reinserting_original_symbol_fails(self) -> None:
        original = r"The model is $M$."
        polished = r"The model is $N$. A separate note contains $M$."
        self.assert_rejected_in_all_modes(original, polished)

    def test_allow_additions_rejects_changed_number_reinserted_elsewhere(self) -> None:
        original = "Latency is 10 ms."
        polished = "Latency is 11 ms. The previous draft reported 10 ms."
        self.assert_pair_fails(original, polished, "--allow-additions")

    def test_environment_type_change_fails(self) -> None:
        original = (
            r"\begin{figure}\caption{Overview.}\label{fig:overview}\end{figure}"
        )
        polished = (
            r"\begin{table}\caption{Overview.}\label{fig:overview}\end{table}"
        )
        self.assert_rejected_in_all_modes(original, polished)

    def test_environment_options_and_table_preamble_are_protected(self) -> None:
        mutations = {
            "placement": (
                r"\begin{figure}[t]Text.\end{figure}",
                r"\begin{figure}[b]Text.\end{figure}",
            ),
            "tabular preamble": (
                r"\begin{tabular}{cc}A&B\end{tabular}",
                r"\begin{tabular}{ccc}A&B&C\end{tabular}",
            ),
        }
        for mutation, (original, polished) in mutations.items():
            with self.subTest(mutation=mutation):
                self.assert_rejected_in_all_modes(original, polished)

    def test_multicolumn_alignment_is_protected_but_cell_text_remains_editable(self) -> None:
        original = r"\begin{tabular}{c}\multicolumn{1}{c}{Old header}\end{tabular}"
        changed_alignment = (
            r"\begin{tabular}{c}\multicolumn{1}{l}{Old header}\end{tabular}"
        )
        polished_text = (
            r"\begin{tabular}{c}\multicolumn{1}{c}{Clear header}\end{tabular}"
        )
        self.assert_rejected_in_all_modes(original, changed_alignment)
        self.assert_pair_passes(original, polished_text)

    def test_multirow_interleaved_layout_arguments_are_protected(self) -> None:
        original = r"\multirow{2}[t]{*}{Stable text.}"
        changed_width = r"\multirow{2}[t]{=}{Stable text.}"
        polished_text = r"\multirow{2}[t]{*}{Clear text.}"
        self.assert_rejected_in_all_modes(original, changed_width)
        self.assert_pair_passes(original, polished_text)

    def test_unbalanced_tex_group_fails_even_when_command_names_match(self) -> None:
        self.assert_rejected_in_all_modes(
            r"\textbf{Safe text.}",
            r"\textbf{Safe text.",
        )
        self.assert_pair_fails("Text.", "Text.}")
        self.assert_pair_passes(r"Escaped \{text\}.", r"Escaped \{clear text\}.")
        self.assert_pair_passes(
            "% unmatched { in a comment\n" + r"\verb|}| Text.",
            "% unmatched { in a comment\n" + r"\verb|}| Clear text.",
        )
        inactive_comment_environment = (
            "\\begin{comment}\n{\n\\end{comment}\nText."
        )
        self.assert_pair_passes(
            inactive_comment_environment,
            inactive_comment_environment,
        )

    def test_malformed_environment_nesting_fails_closed(self) -> None:
        malformed = r"\begin{itemize}\item Text.\end{enumerate}"
        self.assert_pair_fails(malformed, malformed)
        self.assert_pair_fails("Text.", r"Text.\end{itemize}")

    def test_visible_theorem_title_can_be_polished_without_structure_change(self) -> None:
        self.assert_pair_passes(
            r"\begin{theorem}[Old wording]Text.\end{theorem}",
            r"\begin{theorem}[Clearer wording]Text.\end{theorem}",
        )
        self.assert_pair_fails(
            r"\begin{theorem}[See \ref{sec:a}]Text.\end{theorem}",
            r"\begin{theorem}[See \ref{sec:b}]Text.\end{theorem}",
        )

    def test_section_command_deletion_fails(self) -> None:
        original = r"\section{Method}\label{sec:method}Method text."
        polished = r"\label{sec:method}Method text."
        self.assert_rejected_in_all_modes(original, polished)

    def test_itemize_environment_deletion_fails(self) -> None:
        original = r"Before.\begin{itemize}\item First.\end{itemize}After."
        polished = "Before. First. After."
        self.assert_rejected_in_all_modes(original, polished)

    def test_label_binding_swap_fails_even_when_key_counts_match(self) -> None:
        original = (
            r"\section{Alpha}\label{sec:alpha}Alpha text."
            r"\section{Beta}\label{sec:beta}Beta text."
        )
        polished = (
            r"\section{Alpha}\label{sec:beta}Alpha text."
            r"\section{Beta}\label{sec:alpha}Beta text."
        )
        self.assert_rejected_in_all_modes(original, polished)

    def test_starred_includegraphics_path_change_fails(self) -> None:
        original = r"\includegraphics*[width=0.8\linewidth]{figures/source.pdf}"
        polished = r"\includegraphics*[width=0.8\linewidth]{figures/replacement.pdf}"
        self.assert_rejected_in_all_modes(original, polished)

    def test_pageref_and_textcite_key_changes_fail(self) -> None:
        mutations = {
            "pageref": (
                r"See page~\pageref{sec:method}.",
                r"See page~\pageref{sec:results}.",
            ),
            "textcite": (
                r"\textcite{smith2024} introduced the method.",
                r"\textcite{jones2025} introduced the method.",
            ),
        }
        for command, (original, polished) in mutations.items():
            with self.subTest(command=command):
                self.assert_rejected_in_all_modes(original, polished)

    def test_nested_reference_in_citation_note_and_volcite_key_are_protected(self) -> None:
        mutations = {
            "nested citation note": (
                r"\cite[see \ref{sec:a}]{smith2024}",
                r"\cite[see \ref{sec:b}]{smith2024}",
            ),
            "volcite key": (
                r"\volcite{2}{smith2024}",
                r"\volcite{2}{jones2025}",
            ),
        }
        for mutation, (original, polished) in mutations.items():
            with self.subTest(mutation=mutation):
                self.assert_rejected_in_all_modes(original, polished)

    def test_plural_citations_and_hyperref_keys_are_protected(self) -> None:
        mutations = {
            "parencites": (
                r"\parencites[see][]{smith2024}{chen2025}",
                r"\parencites[see][]{smith2024}{jones2026}",
            ),
            "hyperref": (
                r"\hyperref[sec:method]{the method}",
                r"\hyperref[sec:results]{the method}",
            ),
        }
        for command, (original, polished) in mutations.items():
            with self.subTest(command=command):
                self.assert_rejected_in_all_modes(original, polished)

    def test_biblatex_volume_and_multicite_keys_are_protected(self) -> None:
        mutations = {
            "volcite interleaved pages": (
                r"\volcite{2}[3]{smith2024}",
                r"\volcite{2}[3]{jones2025}",
            ),
            "volcite with prenote and pages": (
                r"\volcite[see]{2}[3]{smith2024}",
                r"\volcite[see]{2}[3]{jones2025}",
            ),
            "volcite nonnumeric locator": (
                r"\volcite[see]{II}[appendix]{smith2024}",
                r"\volcite[see]{II}[supplement]{smith2024}",
            ),
            "pvolcite family": (
                r"\pvolcite{2}{smith2024}",
                r"\pvolcite{2}{jones2025}",
            ),
            "ftvolcite family": (
                r"\ftvolcite{2}{smith2024}",
                r"\ftvolcite{2}{jones2025}",
            ),
            "multicite global note": (
                r"\parencites(See){smith2024}{doe2025}",
                r"\parencites(See){jones2026}{doe2025}",
            ),
            "volume multicite global notes": (
                r"\volcites(pre)(post){2}{smith2024}{3}{doe2025}",
                r"\volcites(pre)(post){2}{jones2026}{3}{doe2025}",
            ),
            "generic biblatex citation command": (
                r"\footfullcite{smith2024}",
                r"\footfullcite{jones2025}",
            ),
        }
        for command, (original, polished) in mutations.items():
            with self.subTest(command=command):
                self.assert_rejected_in_all_modes(original, polished)

    def test_literal_source_is_hard_protected(self) -> None:
        original = (
            "\\label{sec:real}\n"
            "\\begin{verbatim}\n"
            "\\label{sec:example_old}\n"
            "\\end{verbatim}\n"
        )
        polished = (
            "\\label{sec:real}\n"
            "\\begin{verbatim}\n"
            "\\label{sec:example_new}\n"
            "\\end{verbatim}\n"
        )
        self.assert_rejected_in_all_modes(original, polished)

    def test_fancyvrb_restore_references_are_protected(self) -> None:
        mutations = {
            "UseVerb": (
                r"\SaveVerb{a}|alpha|\SaveVerb{b}|beta|\UseVerb{a}",
                r"\SaveVerb{a}|alpha|\SaveVerb{b}|beta|\UseVerb{b}",
            ),
            "UseVerbatim": (
                r"\UseVerbatim{example-a}",
                r"\UseVerbatim{example-b}",
            ),
            "BUseVerbatim": (
                r"\BUseVerbatim{example-a}",
                r"\BUseVerbatim{example-b}",
            ),
            "LUseVerbatim": (
                r"\LUseVerbatim{example-a}",
                r"\LUseVerbatim{example-b}",
            ),
        }
        for command, (original, polished) in mutations.items():
            with self.subTest(command=command):
                self.assert_rejected_in_all_modes(original, polished)

    def test_comment_and_literal_boundaries_are_hard_protected(self) -> None:
        mutations = {
            "plain prose commented out": (
                "Critical conclusion.\n",
                "% Critical conclusion.\n",
            ),
            "comment environment removed": (
                "\\begin{comment}\nHidden text.\n\\end{comment}\n",
                "Hidden text.\n",
            ),
            "comment converted to verbatim": (
                "\\begin{comment}\nHidden text.\n\\end{comment}\n",
                "\\begin{verbatim}\nHidden text.\n\\end{verbatim}\n",
            ),
            "inline verb star changed": (
                r"Use \verb|literal text|.",
                r"Use \verb*|literal text|.",
            ),
            "listing language changed": (
                r"Use \lstinline[language=Python]|value|.",
                r"Use \lstinline[language=C]|value|.",
            ),
            "fancyvrb inline literal changed": (
                r"Use \Verb|alpha|.",
                r"Use \Verb|beta|.",
            ),
            "fancyvrb saved literal changed": (
                r"Use \SaveVerb{name}|alpha|.",
                r"Use \SaveVerb{name}|beta|.",
            ),
            "minted inline literal changed": (
                r"Use \mint{python}|alpha|.",
                r"Use \mint{python}|beta|.",
            ),
            "comment moved across math": (
                "% keep\nText $M$.",
                "Text $M$.\n% keep",
            ),
            "inline literal moved across math": (
                r"Use \verb|alpha| before $M$.",
                r"Use $M$ before \verb|alpha|.",
            ),
            "inline comment changed to whole-line comment": (
                "alpha%\nbeta",
                "alpha\n%\nbeta",
            ),
        }
        for mutation, (original, polished) in mutations.items():
            with self.subTest(mutation=mutation):
                self.assert_rejected_in_all_modes(original, polished)

    def test_approved_symbol_map_allows_only_the_declared_math_replacement(self) -> None:
        self.assert_pair_passes(
            r"The model is $y=Mx$.",
            r"The model is $y=Nx$.",
            "--approved-symbol-map",
            "M=N",
        )
        self.assert_pair_passes(
            r"The model is \ensuremath{M}.",
            r"The model is \ensuremath{N}.",
            "--approved-symbol-map",
            "M=N",
        )

    def test_approved_symbol_map_option_is_repeatable(self) -> None:
        self.assert_pair_passes(
            r"The model is $y=Mx$.",
            r"The model is $z=Nu$.",
            "--approved-symbol-map",
            "M=N",
            "--approved-symbol-map",
            "x=u",
            "--approved-symbol-map",
            "y=z",
        )

    def test_approved_symbol_map_rejects_numeric_mapping(self) -> None:
        self.assert_pair_fails(
            r"The model uses $x_1$.",
            r"The model uses $x_1$.",
            "--approved-symbol-map",
            "1=2",
        )
        self.assert_pair_fails(
            r"The objective contains $a+b$.",
            r"The objective contains $a-b$.",
            "--approved-symbol-map",
            "+=-",
        )
        for mapping in (
            "x²=x³",
            "½=⅓",
            "①=②",
            "one=two",
            "Type II=Type I",
            "USD=EUR",
            r"\%=\alpha",
            r"\mathbf{USD}=\mathbf{EUR}",
            r"\mathbf{\%}=\mathbf{pp}",
        ):
            with self.subTest(mapping=mapping):
                self.assert_pair_fails(
                    r"The model uses $x$.",
                    r"The model uses $x$.",
                    "--approved-symbol-map",
                    mapping,
                )

        self.assert_pair_passes(
            r"The coefficient is $\kappa$.",
            r"The coefficient is $\lambda$.",
            "--approved-symbol-map",
            r"\kappa=\lambda",
        )

    def test_approved_symbol_map_rejects_any_extra_math_change(self) -> None:
        self.assert_pair_fails(
            r"The model is $y=Mx+z$.",
            r"The model is $y=Nx+w$.",
            "--approved-symbol-map",
            "M=N",
        )

    def test_approved_symbol_map_rejects_unrelated_prose_change(self) -> None:
        self.assert_pair_fails(
            r"The model is $y=Mx$.",
            r"Our model is $y=Nx$.",
            "--approved-symbol-map",
            "M=N",
        )

    def test_approved_symbol_map_cannot_change_math_text_or_protected_keys(self) -> None:
        mutations = {
            "text-mode acronym": (
                r"Metric $\text{MSE}$ and matrix $M$.",
                r"Metric $\text{NSE}$ and matrix $N$.",
            ),
            "label key": (
                r"\begin{equation}M\label{eq:M}\end{equation}",
                r"\begin{equation}N\label{eq:N}\end{equation}",
            ),
        }
        for mutation, (original, polished) in mutations.items():
            with self.subTest(mutation=mutation):
                self.assert_pair_fails(
                    original,
                    polished,
                    "--approved-symbol-map",
                    "M=N",
                )

    def test_approved_symbol_map_rejects_comment_or_literal_changes(self) -> None:
        original = "% keep this note\n" + r"\verb|M| and $M$."
        polished = "% changed note\n" + r"\verb|N| and $N$."
        self.assert_pair_fails(
            original,
            polished,
            "--approved-symbol-map",
            "M=N",
        )
        for command in ("Verb", "SaveVerb{name}", "mint{python}"):
            with self.subTest(command=command):
                self.assert_pair_fails(
                    rf"\{command}|$M$| and $M$.",
                    rf"\{command}|$N$| and $N$.",
                    "--approved-symbol-map",
                    "M=N",
                )
                self.assert_pair_passes(
                    rf"\{command}|$M$| and $M$.",
                    rf"\{command}|$M$| and $N$.",
                    "--approved-symbol-map",
                    "M=N",
                )

    def test_approved_symbol_map_preserves_literal_whitespace_exactly(self) -> None:
        self.assert_pair_fails(
            r"\verb|a b| and $M$.",
            r"\verb|a  b| and $N$.",
            "--approved-symbol-map",
            "M=N",
        )
        self.assert_pair_fails(
            "% exact  comment\nState $M$.",
            "% exact comment\nState $N$.",
            "--approved-symbol-map",
            "M=N",
        )
        self.assert_pair_passes(
            "State\n  $M$.\n",
            "State $N$.\n",
            "--approved-symbol-map",
            "M=N",
        )
        self.assert_pair_fails(
            r"\mintinline{python}|a b| and $M$.",
            r"\mintinline{python}|a  b| and $N$.",
            "--approved-symbol-map",
            "M=N",
        )

    def test_approved_symbol_map_does_not_rewrite_math_names(self) -> None:
        for command in ("operatorname", "mathrm"):
            with self.subTest(command=command):
                self.assert_pair_fails(
                    rf"Metric $\{command}{{MSE}}$ and matrix $M$.",
                    rf"Metric $\{command}{{NSE}}$ and matrix $N$.",
                    "--approved-symbol-map",
                    "M=N",
                )

    def test_bibliography_display_number_does_not_trigger_intrinsic_style_failure(self) -> None:
        source = (
            r"\begin{thebibliography}{1}"
            r"\bibitem{smith} Figure 1 revisited."
            r"\end{thebibliography}"
        )
        self.assert_pair_passes(source, source)
        self.assert_pair_fails(source, source.replace("Figure 1", "Figure 2"))
        self.assert_pair_fails(source, source.replace("{smith}", "{jones}"))

    def write_nested_project(self, root: Path, *, deepest_symbol: str = "M") -> None:
        parts = root / "parts"
        parts.mkdir(parents=True)
        (root / "main.tex").write_text(
            "\\documentclass{article}\n"
            "\\begin{document}\n"
            "\\input{parts/input_child}\n"
            "\\end{document}\n",
            encoding="utf-8",
        )
        # Nested paths intentionally remain relative to the main-file project root,
        # matching TeX's normal include lookup rather than the including file's directory.
        (parts / "input_child.tex").write_text(
            "Input child.\\include{parts/include_child}\n", encoding="utf-8"
        )
        (parts / "include_child.tex").write_text(
            "Include child.\\subfile{parts/subfile_child}\n", encoding="utf-8"
        )
        (parts / "subfile_child.tex").write_text(
            f"Deep state $y={deepest_symbol}x$.\n", encoding="utf-8"
        )

    def run_projects(
        self,
        mutate_polished_project: Callable[[Path], None] | None = None,
        *,
        project_mode: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            original_root = root / "original"
            polished_root = root / "polished"
            self.write_nested_project(original_root)
            self.write_nested_project(polished_root)
            if mutate_polished_project is not None:
                mutate_polished_project(polished_root)
            command = [
                sys.executable,
                str(SCRIPT_PATH),
                str(original_root / "main.tex"),
                str(polished_root / "main.tex"),
            ]
            if project_mode:
                command.append("--project")
            return subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )

    def test_project_mode_recurses_from_main_root_through_all_include_commands(self) -> None:
        unchanged = self.run_projects()
        self.assertEqual(unchanged.returncode, 0, unchanged.stdout + unchanged.stderr)

        def mutate_deepest_file(polished_root: Path) -> None:
            (polished_root / "parts" / "subfile_child.tex").write_text(
                "Deep state $y=Nx$.\n", encoding="utf-8"
            )

        changed = self.run_projects(mutate_deepest_file)
        self.assertNotEqual(changed.returncode, 0, changed.stdout + changed.stderr)

    def test_single_file_mode_does_not_recurse_without_project_flag(self) -> None:
        def mutate_deepest_file(polished_root: Path) -> None:
            (polished_root / "parts" / "subfile_child.tex").write_text(
                "Deep state $y=Nx$.\n", encoding="utf-8"
            )

        result = self.run_projects(mutate_deepest_file, project_mode=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_project_mode_fails_when_included_file_is_missing(self) -> None:
        def remove_include_target(polished_root: Path) -> None:
            (polished_root / "parts" / "include_child.tex").unlink()

        result = self.run_projects(remove_include_target)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_project_mode_recurses_through_import_family(self) -> None:
        commands = (
            "import",
            "import*",
            "subimport",
            "inputfrom",
            "includefrom",
            "subinputfrom",
            "subincludefrom",
        )
        for command in commands:
            with self.subTest(command=command), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                for side, symbol in (("original", "M"), ("polished", "N")):
                    project = root / side
                    sections = project / "sections"
                    sections.mkdir(parents=True)
                    (project / "main.tex").write_text(
                        rf"\{command}{{sections/}}{{method.tex}}" + "\n",
                        encoding="utf-8",
                    )
                    (sections / "method.tex").write_text(
                        f"State $y={symbol}x$.\n",
                        encoding="utf-8",
                    )
                result = subprocess.run(
                    [
                        sys.executable,
                        str(SCRIPT_PATH),
                        str(root / "original" / "main.tex"),
                        str(root / "polished" / "main.tex"),
                        "--project",
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertNotEqual(
                    result.returncode, 0, result.stdout + result.stderr
                )

    def run_custom_project_pair(
        self,
        writer: Callable[[Path, str], None],
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for side, symbol in (("original", "M"), ("polished", "N")):
                project = root / side
                project.mkdir(parents=True)
                writer(project, symbol)
            return subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    str(root / "original" / "main.tex"),
                    str(root / "polished" / "main.tex"),
                    "--project",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

    def test_import_context_controls_nested_plain_and_sub_imports(self) -> None:
        def write_plain_child(project: Path, symbol: str) -> None:
            sections = project / "sections"
            sections.mkdir()
            (project / "main.tex").write_text(
                r"\import{sections/}{method.tex}" + "\n", encoding="utf-8"
            )
            (sections / "method.tex").write_text(
                r"\input{helper.tex}" + "\n", encoding="utf-8"
            )
            (project / "helper.tex").write_text("Root $x$.\n", encoding="utf-8")
            (sections / "helper.tex").write_text(
                f"Imported ${symbol}$.\n", encoding="utf-8"
            )

        result = self.run_custom_project_pair(write_plain_child)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

        def write_subimport(project: Path, symbol: str) -> None:
            nested = project / "sections" / "nested"
            nested.mkdir(parents=True)
            (project / "main.tex").write_text(
                r"\import{sections/}{method.tex}" + "\n", encoding="utf-8"
            )
            (project / "sections" / "method.tex").write_text(
                r"\subimport{nested/}{deep.tex}" + "\n", encoding="utf-8"
            )
            (nested / "deep.tex").write_text(
                f"Nested ${symbol}$.\n", encoding="utf-8"
            )

        result = self.run_custom_project_pair(write_subimport)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_full_import_inside_imported_file_resets_to_project_root(self) -> None:
        def writer(project: Path, symbol: str) -> None:
            (project / "sections" / "common").mkdir(parents=True)
            (project / "common").mkdir()
            (project / "main.tex").write_text(
                r"\import{sections/}{method.tex}" + "\n", encoding="utf-8"
            )
            (project / "sections" / "method.tex").write_text(
                r"\import{common/}{deep.tex}" + "\n", encoding="utf-8"
            )
            (project / "sections" / "common" / "deep.tex").write_text(
                "Wrong-path $x$.\n", encoding="utf-8"
            )
            (project / "common" / "deep.tex").write_text(
                f"Root-reset ${symbol}$.\n", encoding="utf-8"
            )

        result = self.run_custom_project_pair(writer)
        self.assertIn("Project traversal: PASS", result.stdout)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_import_stack_falls_back_through_previous_import_directory(self) -> None:
        def writer(project: Path, symbol: str) -> None:
            nested = project / "abc" / "nested"
            nested.mkdir(parents=True)
            (project / "main.tex").write_text(
                r"\import{abc/}{one.tex}" + "\n", encoding="utf-8"
            )
            (project / "abc" / "one.tex").write_text(
                r"\subimport{nested/}{two.tex}" + "\n", encoding="utf-8"
            )
            (nested / "two.tex").write_text(
                r"\input{three.tex}" + "\n", encoding="utf-8"
            )
            (project / "three.tex").write_text("Wrong-root $x$.\n", encoding="utf-8")
            (project / "abc" / "three.tex").write_text(
                f"Previous-base ${symbol}$.\n", encoding="utf-8"
            )

        result = self.run_custom_project_pair(writer)
        self.assertIn("Project traversal: PASS", result.stdout)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_subimport_target_falls_back_to_previous_import_directory(self) -> None:
        def writer(project: Path, symbol: str) -> None:
            (project / "abc" / "nested").mkdir(parents=True)
            (project / "main.tex").write_text(
                r"\import{abc/}{one.tex}" + "\n", encoding="utf-8"
            )
            (project / "abc" / "one.tex").write_text(
                r"\subimport{nested/}{two.tex}" + "\n", encoding="utf-8"
            )
            (project / "abc" / "two.tex").write_text(
                f"Fallback target ${symbol}$.\n", encoding="utf-8"
            )

        result = self.run_custom_project_pair(writer)
        self.assertIn("Project traversal: PASS", result.stdout)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_subfile_establishes_directory_context_for_nested_input(self) -> None:
        def writer(project: Path, symbol: str) -> None:
            chapter = project / "chapter"
            chapter.mkdir()
            (project / "main.tex").write_text(
                r"\subfile{chapter/section.tex}" + "\n", encoding="utf-8"
            )
            (chapter / "section.tex").write_text(
                r"\input{text.tex}" + "\n", encoding="utf-8"
            )
            (project / "text.tex").write_text("Wrong-root $x$.\n", encoding="utf-8")
            (chapter / "text.tex").write_text(
                f"Subfile-local ${symbol}$.\n", encoding="utf-8"
            )

        result = self.run_custom_project_pair(writer)
        self.assertIn("Project traversal: PASS", result.stdout)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_project_mode_recurses_through_subfileinclude(self) -> None:
        def writer(project: Path, symbol: str) -> None:
            chapter = project / "chapter"
            chapter.mkdir()
            (project / "main.tex").write_text(
                r"\subfileinclude{chapter/section.tex}" + "\n",
                encoding="utf-8",
            )
            (chapter / "section.tex").write_text(
                f"Changed math ${symbol}$.\n", encoding="utf-8"
            )

        result = self.run_custom_project_pair(writer)
        self.assertIn("Project traversal: PASS", result.stdout)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_subfile_family_target_falls_back_to_previous_import_directory(self) -> None:
        for command in ("subfile", "subfileinclude"):
            with self.subTest(command=command):
                def writer(project: Path, symbol: str) -> None:
                    (project / "abc" / "nested").mkdir(parents=True)
                    (project / "main.tex").write_text(
                        r"\import{abc/}{one.tex}" + "\n", encoding="utf-8"
                    )
                    (project / "abc" / "one.tex").write_text(
                        rf"\{command}{{nested/two.tex}}" + "\n",
                        encoding="utf-8",
                    )
                    (project / "abc" / "two.tex").write_text(
                        f"Fallback target ${symbol}$.\n", encoding="utf-8"
                    )

                result = self.run_custom_project_pair(writer)
                self.assertIn("Project traversal: PASS", result.stdout)
                self.assertNotEqual(
                    result.returncode, 0, result.stdout + result.stderr
                )

    def test_empty_static_import_directory_is_supported(self) -> None:
        def writer(project: Path, symbol: str) -> None:
            (project / "main.tex").write_text(
                r"\import{}{child.tex}" + "\n", encoding="utf-8"
            )
            (project / "child.tex").write_text(
                f"Child ${symbol}$.\n", encoding="utf-8"
            )

        result = self.run_custom_project_pair(writer)
        self.assertIn("Project traversal: PASS", result.stdout)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_project_mode_fails_closed_on_dynamic_import(self) -> None:
        def writer(project: Path, symbol: str) -> None:
            (project / "main.tex").write_text(
                r"\import{\sectiondir}{method.tex}" + "\n", encoding="utf-8"
            )

        result = self.run_custom_project_pair(writer)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("dynamic or empty", result.stdout)


if __name__ == "__main__":
    unittest.main()
