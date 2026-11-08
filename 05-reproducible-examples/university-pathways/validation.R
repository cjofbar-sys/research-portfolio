# R validation of Python-generated synthetic university pathways
# Methodological cross-check, not a separate empirical analysis.
# Usage: Rscript validation.R results/synthetic_students.csv results/synthetic_semesters.csv
# Requires: base R + stats. No packages beyond the standard R distribution.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) {
  stop("Pass Python-generated students and semesters CSV paths")
}
s <- read.csv(args[1], stringsAsFactors = FALSE)
p <- read.csv(args[2], stringsAsFactors = FALSE)
stopifnot(nrow(s) == 1170, length(unique(s$student_id)) == 1170)
stopifnot(all(s$timely_graduation %in% c(0, 1)))
stopifnot(all(s$graduated %in% c(0, 1)))
stopifnot(all(p$credits_earned >= 0))

cat("SYNTHETIC DATA ONLY — not empirical university records\n")
cat("Entrants:", nrow(s), "\n")
cat("Timely graduation:", mean(s$timely_graduation), "\n")
cat("Graduation by semester 12:", mean(s$graduated), "\n")

# Independent, transparent competing-risks first-event life table.
risk <- nrow(s)
survival <- 1
cif_grad <- 0
cif_withdraw <- 0
life <- data.frame()
for (t in seq_len(12)) {
  g <- sum(s$event == "graduation" & s$event_time == t)
  w <- sum(s$event == "withdrawal" & s$event_time == t)
  if (risk > 0) {
    cif_grad <- cif_grad + survival * g / risk
    cif_withdraw <- cif_withdraw + survival * w / risk
    survival <- survival * (1 - (g + w) / risk)
  }
  life <- rbind(life, data.frame(
    semester=t, at_risk=risk, graduation_cif=cif_grad,
    withdrawal_cif=cif_withdraw))
  risk <- risk - g - w
}
stopifnot(abs(tail(life$graduation_cif, 1) - mean(s$graduated)) < 1e-8)

# Independent binomial estimation for the first-generation contrast;
# model specification matches the Python GLM with campus/cohort indicators.
s$campus <- factor(s$campus)
s$cohort <- factor(s$cohort)
fit <- glm(
  timely_graduation ~ first_gen + preparation + support + campus + cohort,
  family = binomial(), data = s)
ci <- suppressMessages(confint.default(fit, parm="first_gen"))
cat("First-generation timely-graduation OR:", exp(coef(fit)["first_gen"]), "\n")
cat("Wald 95% CI:", exp(ci), "\n")
cat("Final competing-risk graduation CIF:", tail(life$graduation_cif, 1), "\n")

# Employment among graduates is conditional on reaching a degree.
grad <- s[s$graduated == 1, ]
employment <- glm(
  employed_6m ~ internship + first_gen + preparation + support + campus,
  family = binomial(), data = grad)
cat("Conditional employment internship OR:", exp(coef(employment)["internship"]), "\n")
cat("No results here are estimates for real students.\n")
