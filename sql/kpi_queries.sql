-- Months to goal
SELECT COUNT(*) AS months_to_goal
FROM (
  SELECT month_end, balance_end,
         SUM(CASE WHEN balance_end >= 20000 THEN 1 ELSE 0 END)
           OVER (ORDER BY month_end) AS reached
  FROM cashflow_monthly
)
WHERE reached = 0;

-- Contribution vs interest split at or before goal month
WITH cutoff AS (
  SELECT MIN(month_end) AS goal_month
  FROM cashflow_monthly
  WHERE balance_end >= 20000
)
SELECT
  SUM(deposits) AS total_contrib,
  SUM(interest) AS total_interest,
  SUM(deposits) + SUM(interest) AS growth
FROM cashflow_monthly
WHERE month_end <= (SELECT goal_month FROM cutoff);
