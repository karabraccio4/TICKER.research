# NVIDIA (NVDA) — Legend Panel Memos

These three investor memos use the same SEC EDGAR annual-filing facts printed by `edgar_buffett.py`. This is a learning demonstration, not investment advice.

## Buffett-style memo

### Verdict: own the business

All three code checks pass. Revenue rose from 26,914 to 215,938, net income rose from 9,752 to 120,067, and owner earnings rose from 8,132 to 96,676.

ROE stayed above the stated 15% screen in every year: 36.6%, 19.8%, 69.2%, 91.9%, and 76.3%. Owner earnings remained positive after capital spending across the full period, supporting a business-quality verdict without a statement about price.

## Graham-style memo

### Verdict: own the business

All three code checks pass. The latest current ratio is 3.91, above the stated 2 threshold. Net income was positive in every year and increased from 9,752 to 120,067.

On these limited screens, the business combines conservative short-term liquidity with earnings growth. This is a screen result rather than a conclusion about price or a margin of safety.

### Threshold decision

I keep the 2 current-ratio threshold because it preserves the conservative liquidity margin built into the Graham screen.

## Burry-style memo

### Verdict: watch it

The leverage check passes: the latest liabilities-to-equity ratio is 0.31, below the stated 2 ceiling. The cash-versus-earnings check fails because operating cash flow does not equal or exceed net income in every year; in the latest year it is 102,718 versus 120,067.

That cash-conversion gap is enough to keep a skeptical verdict at watch it, even though the latest leverage result is contained. This panel does not establish whether the shares are attractively priced.
