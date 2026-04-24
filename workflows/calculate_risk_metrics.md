# Workflow: Calculate Risk Metrics

## Objective
Compute quantitative financial health indicators and flag risk zones.

## Required Inputs
- `.tmp/{ticker}_fundamentals.json` - Must contain: market cap, debt, equity, revenue, EBIT, cash flow, total assets

## Tools to Execute (in sequence)
1. `tools/calculate_altman_zscore.py` - Bankruptcy prediction score
2. `tools/calculate_debt_ratios.py` - Leverage and liquidity metrics

## Expected Outputs
- `.tmp/{ticker}_analysis.json` - Contains:
  - `altman_zscore`: Numeric value (typically -4 to 8+)
  - `zscore_zone`: "green" (>3.0), "yellow" (1.8-3.0), "red" (<1.8)
  - `debt_to_equity`: Ratio value
  - `debt_zone`: "green" (<1.0), "yellow" (1.0-2.0), "red" (>2.0)
  - `ocf_to_ni`: Operating Cash Flow / Net Income ratio
  - `ocf_flag`: true if OCF << Net Income (earnings quality concern)
  - `risk_flags`: Array of warning messages

## Execution Steps
1. Load `.tmp/{ticker}_fundamentals.json`
2. Validate required fields present (if missing → flag as "Insufficient data")
3. Run calculate_altman_zscore.py
4. Run calculate_debt_ratios.py
5. Aggregate results into single `.tmp/{ticker}_analysis.json`
6. Generate risk_flags array based on thresholds

## Altman Z-Score Calculation
Formula: `Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 1.0*X5`

Where:
- X1 = Working Capital / Total Assets
- X2 = Retained Earnings / Total Assets
- X3 = EBIT / Total Assets
- X4 = Market Value of Equity / Total Liabilities
- X5 = Sales (Revenue) / Total Assets

**Interpretation**:
- Z > 3.0: Safe zone (low bankruptcy risk)
- 1.8 < Z < 3.0: Gray zone (caution)
- Z < 1.8: Distress zone (high bankruptcy risk)

## Debt Ratio Thresholds
| Metric | Green | Yellow | Red |
|--------|-------|--------|-----|
| Debt/Equity | < 1.0 | 1.0-2.0 | > 2.0 |
| OCF/Net Income | ≥ 0.8 | 0.5-0.8 | < 0.5 |
| Current Ratio | > 1.5 | 1.0-1.5 | < 1.0 |

## Risk Flags Generated
Automatically flag if:
- Altman Z-Score < 1.8 → "High bankruptcy risk"
- Debt/Equity > 2.0 → "Excessive leverage"
- OCF/Net Income < 0.5 → "Earnings quality concern (cash flow weak)"
- Negative revenue growth 2+ years → "Declining revenue trend"
- Current Ratio < 1.0 → "Liquidity risk"

## Error Handling
- **Missing data fields**: Return "N/A" for that metric, flag as "Insufficient data for calculation"
- **Division by zero**: (e.g., Total Assets = 0) → Return Z-Score as "N/A", flag error
- **Negative denominators**: (unusual but possible) → Flag as data quality issue
- **Pre-revenue company**: EBIT, revenue = 0 → Z-Score invalid, note in report

## Validation
- Cross-check Z-Score against known examples:
  - AAPL (healthy): Expected Z > 5.0
  - Distressed company: Expected Z < 1.8
- Spot-check calculation: Re-run formula manually for 1 test case

## Performance Targets
- **Execution time**: <500ms (pure calculation, no API calls)
- **Accuracy**: ±2% tolerance on Z-Score vs. manual calculation

## Notes
- Altman Z-Score designed for manufacturing companies; may be less accurate for tech/services
- For non-US companies, adjust formula (Altman Z'-Score variant exists)
- Update thresholds based on industry (e.g., utilities tolerate higher debt)
- If Z-Score calculation fails, analysis can still proceed with debt ratios only
