# Video Walkthrough Script (5-7 Minutes)

*Natural, conversational explanation for video presentation*

---

## Opening (30 seconds)

Hey everyone. So for this challenge, I built an AI-powered investment diligence engine. The goal was to help analysts quickly evaluate whether a company is worth investing in by automatically gathering financial data, analyzing risks, and providing actionable recommendations.

Let me walk you through how I approached this, what I built, and how it actually works.

---

## My Implementation Approach (1 minute)

So when I first looked at this problem, I knew I had about 4 hours to build something real. Not just slides—an actual working system.

My first thought was: what would I actually use if I were doing investment research? I'd want something that pulls live data, runs the numbers, checks sentiment, and gives me a clear recommendation. Not just raw data dumps.

So I decided to build this around three core risk detections:
- **Financial risk** – using metrics like the Altman Z-Score and debt ratios to see if a company is financially healthy
- **Sentiment risk** – analyzing recent news to understand market perception
- **Legal risk** – checking SEC filings for any red flags

The key was making this real-time. Every analysis runs fresh—current stock prices, latest news from the past 30 days, up-to-date financial statements. No stale cached data from weeks ago.

---

## Architecture Choices (1.5 minutes)

For the architecture, I went with something I call the WAT framework—Workflows, Agents, and Tools. It's basically about separating concerns so the system stays reliable and maintainable.

Here's how it works:

**Workflows** are just markdown files—plain English instructions that describe what to do. Think of them as SOPs. For example, one workflow says "first fetch stock fundamentals, then calculate risk metrics, then analyze sentiment."

**The Agent** is the orchestrator—it reads those workflows and executes them step by step. This is where I use Claude AI to make intelligent decisions, like synthesizing all the data into a final investment recommendation.

**Tools** are deterministic Python scripts that do the heavy lifting—things like calling Yahoo Finance for stock data, fetching news articles, calculating the Z-Score formula. These don't change their behavior; they just execute reliably.

Why this structure? Because when AI tries to do everything directly, accuracy drops fast. But when you give AI the job of coordination and decision-making, and use scripts for the actual execution, you get both intelligence and reliability.

---

## Delivery Phases (1 minute)

Now, if I were building this for production, I'd break it into phases.

**Phase 1** would be the MVP—exactly what I built here. Core functionality: fetch data, run risk analysis, provide recommendations. Get something working end-to-end that analysts can actually use.

**Phase 2** would be about scale and polish—better error handling, caching strategies, maybe support for international markets, more sophisticated financial models.

**Phase 3** would add advanced features—things like portfolio analysis across multiple stocks, historical trend analysis, automated alerts when risk profiles change.

But for this prototype, I stayed laser-focused on Phase 1. I needed to prove the concept works before worrying about bells and whistles.

---

## The Prototype I Built (1.5 minutes)

Okay, so what does the actual prototype do?

You open up the web interface—built with Streamlit—and you pick a stock. Let's say you choose Microsoft or Google. You hit "Analyze" and the system kicks off.

Behind the scenes, it's running five steps in sequence:

1. **Fetches company data** – pulls fundamentals from Yahoo Finance, tries to grab SEC filings
2. **Calculates risk metrics** – runs the Altman Z-Score calculation, computes debt ratios, checks liquidity
3. **Analyzes sentiment** – fetches news from the past 30 days, scans for positive and negative keywords, scores the sentiment
4. **Generates AI synthesis** – sends all that data to Claude and asks it to make sense of everything
5. **Exports reports** – saves everything to JSON files that could eventually go to Google Sheets or Slides

The whole thing takes about 20-25 seconds. When it's done, you get a clean dashboard showing:
- Financial health metrics with color-coded zones (green = safe, red = distress)
- Altman Z-Score with component breakdown
- Debt analysis
- News sentiment summary
- An AI recommendation: BUY, HOLD, or SELL
- Confidence score out of 10
- Specific reasoning and red flags

Everything updates in real-time. If you analyze the same stock tomorrow, you'll get fresh data reflecting the current market.

---

## Priorities Due to Time Constraints (45 seconds)

Now, with only 4 hours, I had to make trade-offs.

What I **prioritized**: Getting the core pipeline working. Real data integration. Accurate calculations. A clean UI that actually demonstrates the value.

What I **deprioritized**: Full SEC filing parsing—I pull metadata but not the entire 10-K document. Google Sheets integration—I built the export logic but used mock data. Advanced error recovery—there's basic fallback, but production would need more.

The goal was to build something you could actually demo and understand how it works, not something that looks finished but doesn't function.

---

## How I Used AI Tools (1 minute)

Throughout this project, I used Claude—both as part of the system and as my development assistant.

**Inside the system**: Claude analyzes all the financial data, sentiment, and metrics to generate the final investment recommendation. It's really good at synthesizing information and providing nuanced reasoning. For example, it might say "strong financials but premium valuation suggests limited upside"—that's the kind of contextual analysis that's hard to code with rules.

**In my workflow**: I used Claude to help me write and debug code, structure the architecture, and think through edge cases. For example, when yfinance data was incomplete, Claude helped me add fallback logic to extract data from quarterly balance sheets instead.

The key is knowing when to use AI versus deterministic code. AI is great for reasoning and synthesis. Deterministic code is better for calculations and data fetching.

---

## What I'd Build Next (45 seconds)

If I had more time, here's what I'd add next:

**First**, full SEC filing analysis—actually parse the 10-K documents and extract management discussion, risk factors, and legal proceedings.

**Second**, comparative analysis—let users compare multiple stocks side-by-side or analyze an entire portfolio.

**Third**, historical tracking—show how a company's risk profile has changed over time, alert when metrics cross thresholds.

**Fourth**, real Google API integration—push results directly to Sheets and Slides so analysts can share with their teams.

But honestly, what I built here is functional and demonstrates the concept. It's not just a prototype that fakes it—it actually works with real data and real AI.

---

## Closing (15 seconds)

So that's the walkthrough. I built a real-time investment diligence engine that combines financial analysis, sentiment analysis, and AI synthesis to help analysts make faster, better-informed decisions.

The code is on GitHub, it's deployed live on Streamlit Cloud, and you can try it yourself right now.

Thanks for watching!

---

## Speaking Tips

- **Pace**: Speak at ~150 words per minute (natural conversational pace)
- **Tone**: Confident but not arrogant. You built something real and you're proud of it.
- **Pauses**: Pause briefly after each section to let concepts sink in
- **Emphasis**: Stress the key points: "real-time," "actually works," "reliable"
- **Gestures**: Point to your screen when showing the UI, use hand gestures to indicate sequence
- **Eye contact**: Look at the camera like you're talking to a person, not reading a script

## Total Word Count
~1,050 words = approximately 7 minutes at natural speaking pace

## Video Structure Suggestion

0:00 - 0:30: Opening  
0:30 - 1:30: Implementation Approach  
1:30 - 3:00: Architecture Choices  
3:00 - 4:00: Delivery Phases  
4:00 - 5:30: The Prototype Demo  
5:30 - 6:15: Priorities & Trade-offs  
6:15 - 7:15: AI Tools Usage & Future Roadmap  
7:15 - 7:30: Closing  

**Recommendation**: Record yourself reading this naturally, then trim down any sections that run long. You can cut some examples or details to hit exactly 5-7 minutes.
