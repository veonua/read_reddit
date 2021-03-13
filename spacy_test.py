import html

from main import norm_doc
from markdown_utils import unmark
from pyutils import hasNumbers
from spacy_magic import make_nlp
from text_utils import norm

nlp = make_nlp()


def test_1():
    in_text = unmark(
        """#Good morning traders and investors of the r/wallstreetbets sub! Welcome to Thursday! Here are your pre-market stock movers & news on this Thursday, February 18, 2021-*****# [5 things to know before the stock market opens Thursday](https://www.cnbc.com/2021/02/18/5-things-to-know-before-the-stock-market-opens-feb-18-2021.html)*****> # 1. Dow set to drop as Walmart declines on disappointing earnings> * U.S. stock futures fell Thursday, after Dow stock Walmart dropped 4.5% in the premarket on disappointing earnings. The Dow Jones Industrial Average on Wednesday erased a 180-point loss and ended 90 points higher for another record close. The S&P 500 and Nasdaq closed slightly lower for the second straight session. The S&P 500 pared losses after minutes from the Fed’s last meeting signaled easy monetary policy for longer with the economy nowhere close to pre-coronavirus levels.> * The Labor Department is set to release its weekly jobless claims report at 8:30 a.m. ET, one hour before the opening bell. Economists expect 773,000 new filings for unemployment benefits for last week. That would be down 20,000 from 793,000 initial claims the prior week, which saw little relief from declining Covid cases.*****> # 2. Walmart missed on earnings, beat on revenue; CEO to boost wages> * Trying to turn pandemic gains into sustained momentum and higher profitability, Walmart on Thursday before-the-bell reported fourth-quarter adjusted earnings of $1.39 per share, which fell short of estimates. Revenue grew by 7.3% to a better-than-expected $152.1 billion. The big-box retailer’s e-commerce sales in the U.S. grew by 69% and its same-store sales in the U.S. grew by 8.6%. Walmart CEO Doug McMillon said the company will boost the wage of U.S. workers, raising the average for hourly employees to above $15 per hour.*****> # 3. What to expect from GameStop hearing with Robinhood, Citadel, Reddit CEOs> * The heads of Robinhood, Reddit, Citadel and Melvin Capital, will be in Washington for Thursday’s highly anticipated GameStop hearing, which is scheduled to begin at noon ET in the House Financial Services Committee. According to prepared remarks, Reddit CEO Steve Huffman will testify that no significant activity on WallStreetBets last month was driven by bots or foreign agents. Keith Gill, the Reddit and YouTube trading star known as “Roaring Kitty,” will defend his social media posts that helped spark a mania in GameStop shares.*****> # 4. How Texas power grid failed and what could stop it from happening again> * More than 500,000 households in Texas are still without power Thursday morning, according to poweroutage.us, following Sunday night’s historic cold and snow that caused the state’s worst blackouts in decades. Millions of people were in the dark at the height of the crisis, which was caused by a confluence of factors. Officials are already calling for investigations. Experts said there are a number of steps that Texas can take to combat future problems, including weatherizing equipment and increasing the amount of excess supply needed to meet peak power demand.*****> # 5. U.S. life expectancy drops a year in pandemic, most since WWII> * Life expectancy in the U.S. dropped a staggering one year during the first half of 2020 as the pandemic caused the first wave of coronavirus deaths. Minorities suffered the biggest impact, with Black Americans losing nearly three years and Hispanics, nearly two years, according to preliminary estimates Thursday from the CDC. “You have to go back to World War II, the 1940s, to find a decline like this,” said Robert Anderson, who oversees the numbers for the CDC. It’s already known that 2020 was the deadliest year in U.S. history, with deaths topping 3 million for the first time.*****#STOCK FUTURES CURRENTLY:######(**[CLICK HERE FOR STOCK FUTURES CHARTS!](https://finviz.com/futures.ashx)**)*****#YESTERDAY'S MARKET MAP:######(**[CLICK HERE FOR YESTERDAY'S MARKET MAP!](https://i.imgur.com/FrLUO2J.png)**)*****#TODAY'S MARKET MAP:######(**[CLICK HERE FOR TODAY'S MARKET MAP!](https://finviz.com/map.ashx)**)*****#YESTERDAY'S S&P SECTORS:######(**[CLICK HERE FOR YESTERDAY'S S&P SECTORS CHART!](https://i.imgur.com/8MNKhv6.png)**)*****#TODAY'S S&P SECTORS:######(**[CLICK HERE FOR TODAY'S S&P SECTORS CHART!](https://finviz.com/groups.ashx)**)*****#TODAY'S ECONOMIC CALENDAR:######(**[CLICK HERE FOR TODAY'S ECONOMIC CALENDAR LINK #1!](https://i.postimg.cc/T3cRcfQL/econcal1.png)**)######(**[CLICK HERE FOR TODAY'S ECONOMIC CALENDAR LINK #2!](https://i.postimg.cc/15wRfpqK/econcal2.png)**)*****#THIS WEEK'S ECONOMIC CALENDAR:######(**[CLICK HERE FOR THIS WEEK'S ECONOMIC CALENDAR!](https://i.imgur.com/wWv2RIG.png)**)*****#THIS WEEK'S UPCOMING IPO'S:######(**[CLICK HERE FOR THIS WEEK'S UPCOMING IPO'S!](https://i.imgur.com/968QLzv.png)**)*****#THIS WEEK'S EARNINGS CALENDAR:######(**[CLICK HERE FOR THIS WEEK'S EARNINGS CALENDAR!](https://i.imgur.com/03Kxnx1.png)**)*****#THIS MORNING'S PRE-MARKET EARNINGS CALENDAR:######(**[CLICK HERE FOR THIS MORNING'S EARNINGS CALENDAR!](https://i.postimg.cc/TP8PttvF/eram0111.jpg)**)*****#EARNINGS RELEASES BEFORE THE OPEN TODAY:######(**[CLICK HERE FOR THIS MORNING'S EARNINGS RELEASES LINK #1!](https://i.imgur.com/eg2VEbG.png)**)######(**[CLICK HERE FOR THIS MORNING'S EARNINGS RELEASES LINK #2!](https://i.imgur.com/DfgMUm2.png)**)*****#EARNINGS RELEASES AFTER THE CLOSE TODAY:######(**[CLICK HERE FOR THIS AFTERNOON'S EARNINGS RELEASES LINK #1!](https://i.imgur.com/AlgBlru.png)**)######(**[CLICK HERE FOR THIS AFTERNOON'S EARNINGS RELEASES LINK #2!](https://i.imgur.com/ozc7nge.png)**)*****#YESTERDAY'S ANALYST UPGRADES/DOWNGRADES:######(**[CLICK HERE FOR YESTERDAY'S ANALYST UPGRADES/DOWNGRADES LINK #1!](https://i.postimg.cc/sfSCc3gj/upgradesdowngrades1.png)**)######(**[CLICK HERE FOR YESTERDAY'S ANALYST UPGRADES/DOWNGRADES LINK #2!](https://i.postimg.cc/VvjyLWVr/upgradesdowngrades2.png)**)*****#YESTERDAY'S INSIDER TRADING FILINGS:######(**[CLICK HERE FOR YESTERDAY'S INSIDER TRADING FILINGS!](https://i.imgur.com/FKuhY48.png)**)*****#TODAY'S DIVIDEND CALENDAR:######(**[CLICK HERE FOR TODAY'S DIVIDEND CALENDAR LINK #1!](https://i.imgur.com/OLqGg4c.png)**)######(**[CLICK HERE FOR TODAY'S DIVIDEND CALENDAR LINK #2!](https://i.imgur.com/sQzqUDu.png)**)######(**[CLICK HERE FOR TODAY'S DIVIDEND CALENDAR LINK #3!](https://i.imgur.com/sWm5TFN.png)**)*****#THIS MORNING'S STOCK NEWS MOVERS:######(**source: [cnbc.com](https://www.cnbc.com/2021/02/18/stocks-making-the-biggest-moves-premarket-walmart-hormel-foods-marriott-others.html)**)*****> **Walmart (WMT)** – Walmart reported adjusted quarterly earnings of $1.39 per share, which includes a 7-cent impact from UK tax repayment. The consensus estimate had been $1.50. Revenue did beat forecasts, and US comparable sales excluding fuel were up 8.6% compared to the 5.8% FactSet estimate. The retailer’s shares are down 5% premarket.> #**STOCK SYMBOL:** WMT> * [CLICK HERE FOR CHART!](http://elite.finviz.com/chart.ashx?t=WMT&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](http://data.cnbc.com/quotes/WMT)**)*****> **Hormel Foods (HRL)** – The food producer’s stock is up 2.2% premarket after earnings matched estimates at 41 cents per share and revenue beat Wall Street forecasts. Hormel also said it is increasingly optimistic about full-year sales and earnings growth.> #**STOCK SYMBOL:** HRL> * [CLICK HERE FOR CHART!](http://elite.finviz.com/chart.ashx?t=HRL&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](http://data.cnbc.com/quotes/HRL)**)*****> **Marriott (MAR)** – Marriott bucked recent trends by hotel chains by beating Street estimates, earning an adjusted 12 cents per share for its latest quarter compared to an 11 cent consensus estimate. Revenue did miss forecasts as the company continues to be impacted by the pandemic.> #**STOCK SYMBOL:** MAR> * [CLICK HERE FOR CHART!](http://elite.finviz.com/chart.ashx?t=MAR&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](http://data.cnbc.com/quotes/MAR)**)*****> **Waste Management (WM)** – Waste Management shares are up 1% premarket after the waste-hauling company beat estimates by 4 cents with an adjusted quarterly profit of $1.13 per share, with revenue beating estimates as well. Waste Management is also raising its dividend by 12 cents on an annual basis to $2.30 per share.> #**STOCK SYMBOL:** WM> * [CLICK HERE FOR CHART!](http://elite.finviz.com/chart.ashx?t=WM&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](http://data.cnbc.com/quotes/WM)**)*****> **Tilray (TLRY)** – Tilray lost an adjusted 2 cents per share for its latest quarter, smaller than the 15 cent loss expected by Wall Street analysts, while the cannabis producer’s revenue was above estimates. The results come ahead of Tilray’s planned merger with rival Aphria (APHA), which it expects to close in the second quarter. The stock is up 4% in premarket action.> #**STOCK SYMBOL:** TLRY> * [CLICK HERE FOR CHART!](http://elite.finviz.com/chart.ashx?t=TLRY&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](http://data.cnbc.com/quotes/TLRY)**)*****> **SunPower (SPWR)** – SunPower doubled consensus estimates with adjusted quarterly earnings of 14 cents per share, although the solar company’s revenue fell short of forecasts. SunPower also issued weaker than expected current quarter guidance, and its shares are down 7.1% in premarket trading.> #**STOCK SYMBOL:** SPWR> * [CLICK HERE FOR CHART!](http://elite.finviz.com/chart.ashx?t=SPWR&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](http://data.cnbc.com/quotes/SPWR)**)*****> **Twilio (TWLO)** - Twilio is up 9.5% premarket after it reported an adjusted profit of 4 cents per share for its latest quarter, surprising analysts who had expected the cloud computing platform provider to report an 8 cents per share loss. Revenue also came in well above Street forecasts, with results helped by recent acquisitions and election-related business as well as what Twilio calls “broad-based diversified strength”.> #**STOCK SYMBOL:** TWLO> * [CLICK HERE FOR CHART!](http://elite.finviz.com/chart.ashx?t=TWLO&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](http://data.cnbc.com/quotes/TWLO)**)*****> **Baidu (BIDU)** – Baidu saw quarterly revenue come in above analyst projections, with the search engine’s ad sales bouncing back and the company’s cloud services seeing increased demand. Baidu shares are down 1.2% this morning.> #**STOCK SYMBOL:** BIDU> * [CLICK HERE FOR CHART!](http://elite.finviz.com/chart.ashx?t=BIDU&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](http://data.cnbc.com/quotes/BIDU)**)*****> **Sleep Number (SNBR)** – Sleep Number shares are surging 12.7% premarket after it reported quarterly earnings of $2.19 per share, beating the consensus estimate of $1.45, with the mattress retailer’s revenue also exceeding estimates. Sleep Number also issued upbeat full-year guidance.> #**STOCK SYMBOL:** SNBR> * [CLICK HERE FOR CHART!](http://elite.finviz.com/chart.ashx?t=SNBR&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](http://data.cnbc.com/quotes/SNBR)**)*****> **Tesla (TSLA)** – Tesla cut prices for the cheaper versions of its Model 3 and Model Y vehicles, although it raised prices for upper-end variants. Shares are down 2% premarket.> #**STOCK SYMBOL:** TSLA> * [CLICK HERE FOR CHART!](http://elite.finviz.com/chart.ashx?t=TSLA&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](http://data.cnbc.com/quotes/TSLA)**)*****> **Nutrien (NTR)** – Nutrien reported better-than-expected earnings for its latest quarter, as the Canadian fertilizer maker saw increased demand amid rising crop prices and plans by farmers to plant more acres this year. The stock is up 3.8% premarket.> #**STOCK SYMBOL:** NTR> * [CLICK HERE FOR CHART!](http://elite.finviz.com/chart.ashx?t=NTR&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](http://data.cnbc.com/quotes/NTR)**)*****> **Fastly (FSLY)** – Fastly shares are under pressure, down 6.2% premarket, after the cloud-platform provider reported better-than-expected earnings and revenue for its latest quarter but issued a lower than expected forecast.> #**STOCK SYMBOL:** FSLY> * [CLICK HERE FOR CHART!](http://elite.finviz.com/chart.ashx?t=FSLY&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](http://data.cnbc.com/quotes/FSLY)**)*****> **Tanger Factory Outlets (SKT)** – The shopping center operator is up 3.1% after reporting a breakeven quarter, compared to forecasts of a 2 cents per share loss, while revenue beat estimates as well. Tanger saw an increase in foot traffic during the quarter, although lower occupancy rates continue to weigh on revenue.> #**STOCK SYMBOL:** SKT> * [CLICK HERE FOR CHART!](http://elite.finviz.com/chart.ashx?t=SKT&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](http://data.cnbc.com/quotes/SKT)**)*****> **Bloomin’ Brands (BLMN)** – The restaurant operator’s shares are down 4.1% premarket after revenue fell below Street forecasts for its latest quarter. The company did report a breakeven quarter on an adjusted basis, compared to forecasts of a 2 cents per share loss.> #**STOCK SYMBOL:** BLMN> * [CLICK HERE FOR CHART!](http://elite.finviz.com/chart.ashx?t=BLMN&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](http://data.cnbc.com/quotes/BLMN)**)*****#**DISCUSS!**What's on everyone's radar for today's trading day ahead here at r/wallstreetbets?*****# **I hope you all have an excellent trading day ahead today on this Thursday, February 18th, 2021! :)**""")
    doc = nlp(in_text)
    text, n, tick = norm_doc(doc)
    assert {'mar', 'tesla', 'hrl', 'fsly', 'twlo', 'wallmart', 'tilray', 'robinhood', 'baidu', 'wm', 'snbr', 'blmn',
            'ntr', 'skt', 'gamestop', 'spwr', 'apha'} == tick
    assert not hasNumbers(text.replace('s&p 500', ''))


def test_2():
    doc = nlp("""LUCID/$CCIV
    Thank you $PLTR - very cool.
    ($CLA/$IPV) Ouster's LIDAR and Apple
    IN SHORT, I LIKE THE STOCK. 
    10$ apple
    Manganese x Energy (MN.V)
    Owlet Baby Care 'Connected Nursery Ecosystem' $OWLT|$SBG MOON BOUND 🌕 via BECKY X 🚀
    I'm collecting the FCH(withdrawal)，$2000 Free Tokens Are Airdropping.
    Motley fool going from spreading FUD and a $1 price target for AMC, to AMC potentially being bought by Amazon: "Parkour!""")

    text, n, tick = norm_doc(doc)
    assert not hasNumbers(text)
    assert not {'mn.v', 'cla', 'ipv', 'palantir', 'amc', 'owlt', "sbg"} == tick


def test_3():
    in_text = unmark(
        """#Good morning traders & investors of the r/wallstreetbets sub! Welcome to Wednesday! Here are your pre-market stock movers & news this AM-*****#[Today's Top Headlines for January 16th, 2019](https://www.cnbc.com/2019/01/16/dow-futures-lower-brexit-deal-fails-more-bank-earnings.html)* Futures were hovering near breakeven this morning as the market evaluated the impact of the failed Brexit vote. The Dow is sitting less than 200 points away from escaping correction. The three U.S. major averages are coming off their highest closes in more than a month. (CNBC)* European markets higher after May's Brexit vote defeat (CNBC)* U.K. Prime Minister Theresa May had placed a motion before lawmakers in the lower house of Parliament, asking them to rubber stamp her withdrawal agreement with the European Union. The bill was rejected by 432 votes to 202, thought to be the largest in U.K. political history. (CNBC)* It's a big morning for bank earnings, with Bank of America (BAC), Bank of New York Mellon (BK), Comerica (CMA), Goldman Sachs (GS), PNC Financial (PNC), and US Bancorp (USB) all set to report. Asset manager BlackRock (BLK) and brokerage firm Charles Schwab (SCHW) will also issue quarterly numbers this morning. After the bell reports today include CSX Corp. (CSX), H.B. Fuller (FUL), and Kinder Morgan (KMI). (CNBC)* BlackRock results fall short of expectations, assets fall back below $6 trillion (CNBC)* Two economic reports out today are housing-related: the Mortgage Bankers Association will be out with its weekly look at mortgage applications at 7 a.m. ET, while the National Association of Home Builders issues its monthly sentiment index at 10 a.m. ET. The Labor Department will issue its December report on import and export prices at 8:30 a.m. ET. (CNBC)* The Federal Reserve issues its Beige Book today, with its region-by-region assessment of the U.S. economy due out at 2 p.m. ET.* The partial government shutdown, which is now entering its 26th day, has exhausted contingency plans and is prompting drastic measures throughout the federal contracting industry, the Wall Street Journal reported.* China's central bank today pumped a net 560 billion yuan, or $83 billion, into its banking system — a record amount of money injected in one day — in a sign that the economy may be facing enormous stress. (CNBC)* Democrats will get a chance today to grill Trump's point person on deregulation when Andrew Wheeler goes to Capitol Hill for his confirmation hearing to be the next permanent administrator of the EPA. (USA Today)* Acting AG Whitaker to testify before Congress (USA Today)* An FBI agent working for Robert Mueller filed a heavily redacted court document aiming to bolster the special counsel's claim that former Trump campaign chief Paul Manafort repeatedly lied to investigators. (CNBC)* Sen. Kirsten Gillibrand, a New York Democrat, announced she is launching an exploratory committee for a White House run. The senator spent so little during the midterms that she was reportedly left with a $10.7 million war chest. (CNBC)* Sears Chairman Eddie Lampert prevailed in a bankruptcy auctionfor the U.S. department store chain with an improved takeover bid of roughly $5.2 billion, according to Reuters citing sources, allowing the 126-year-old retailer to keep its doors open.* Snap (SNAP) announced that CFO Tim Stone will be stepping downto pursue other opportunities. It also said it would post results that are "slightly favorable" to the top end of its previous guidance when it reports its earnings. (CNBC)* Microsoft (MSFT) announced it has signed a multiyear deal with Walgreens Boots Alliance (WBA) that includes exploring digital health opportunities within stores and developing software for managing patient engagement. (CNBC)* Apple (AAPL) launched three new smart battery cases for its newest iPhones. They cost $129, and it's the first time Apple has launched a battery case since the one it first began selling for the iPhone 6/iPhone 6s. (CNBC)*****#STOCK FUTURES CURRENTLY:######(**[CLICK HERE FOR STOCK FUTURES CHARTS RIGHT NOW!](http://finviz.com/futures.ashx)**)*****#YESTERDAY'S MARKET MAP:######(**[CLICK HERE FOR YESTERDAY'S MARKET MAP!](https://i.imgur.com/LN5kzvp.png)**)*****#TODAY'S MARKET MAP:######(**[CLICK HERE FOR TODAY'S MARKET MAP!](https://finviz.com/map.ashx)**)*****#YESTERDAY'S S&P SECTORS:######(**[CLICK HERE FOR YESTERDAY'S S&P SECTORS CHART!](https://i.imgur.com/TKLW3qd.png)**)*****#TODAY'S S&P SECTORS:######(**[CLICK HERE FOR TODAY'S S&P SECTORS CHART!](https://finviz.com/groups.ashx)**)*****#TODAY'S ECONOMIC CALENDAR:######(**[CLICK HERE FOR TODAY'S ECONOMIC CALENDAR!](https://i.imgur.com/5FkBWmk.png)**)*****#THIS WEEK'S ECONOMIC CALENDAR:######(**[CLICK HERE FOR THIS WEEK'S ECONOMIC CALENDAR!](https://i.imgur.com/PTQaYPx.png)**)*****#THIS WEEK'S UPCOMING IPO'S:######(**[CLICK HERE FOR THIS WEEK'S UPCOMING IPO'S!]()**)NONE.*****#THIS WEEK'S EARNINGS CALENDAR:*($NFLX $C $BAC $JPM $UNH $DAL $WFC $GS $BLK $MS $AXP $AA $SJR $SLB $SNV $INFO $FRC $FAST $BK $PNC $USB $CSX $KMI $BBT$CMA $UAL $TEAM $KEY $CBSH $MTB $VFC $JBHT $SASR $STI $PRGS $FULT $HAFC $HOMB $PTE $RF $OZK $PBCT $WNS $PLXS)*######(**[CLICK HERE FOR THIS WEEK'S EARNINGS CALENDAR!](https://i.imgur.com/m6mH7IN.png)**)*****#THIS MORNING'S PRE-MARKET EARNINGS CALENDAR:*($BAC $GS $BLK $BK $USB $UAL $PNC $CMA $FULT $HAFC $PNFP)*######(**[CLICK HERE FOR THIS MORNING'S EARNINGS CALENDAR!](https://i.imgur.com/W18o142.jpg)**)*****#THIS AFTERNOON'S POST-MARKET EARNINGS CALENDAR:*()*######(**[CLICK HERE FOR THIS AFTERNOON'S EARNINGS CALENDAR!]()**)T.B.A.*****#EARNINGS RELEASES BEFORE THE OPEN TODAY:######(**[CLICK HERE FOR THIS MORNING'S EARNINGS RELEASES!](https://i.imgur.com/SIpUAdB.png)**)*****#EARNINGS RELEASES AFTER THE CLOSE TODAY:######(**[CLICK HERE FOR THIS AFTERNOON'S EARNINGS RELEASES!](https://i.imgur.com/fBgvUMw.png)**)*****#THIS MORNING'S ANALYST UPGRADES/DOWNGRADES:######(**[CLICK HERE FOR THIS MORNING'S UPGRADES/DOWNGRADES!](https://i.imgur.com/OOUUPy8.png)**)*****#THIS MORNING'S INSIDER TRADING FILINGS:######(**[CLICK HERE FOR THIS MORNING'S INSIDER TRADING FILINGS!](https://i.imgur.com/oh9xgUu.png)**)*****#TODAY'S DIVIDEND CALENDAR:######(**[CLICK HERE FOR TODAY'S DIVIDEND CALENDAR!](https://i.imgur.com/Pxeoxx9.png)**)*****#THIS MORNING'S MOST ACTIVE TRENDING TICKERS:* NBEV* BAC* GS* SNAP* F* PCG* FDC* MBOT* FISV* XLF* VHC* PNC* BLK* USB* EFII* BK* JWN* KNDI* SHOP* UAL* KO* NTNX* PLAB* CSX* DIS* UGAZ* CMG* NFLX* QCOM* NLY*****#THIS MORNING'S STOCK NEWS MOVERS:######(**source: [cnbc.com](https://www.cnbc.com/2019/01/16/stocks-making-the-biggest-moves-premarket-fdc-bac-gs-blk--more.html)**)*****> **First Data** – The financial technology company will be acquired by Fiserv in an all-stock deal with an equity value of $22 billion, or $22.74 per share. First Data had closed yesterday at $17.54.> #**STOCK SYMBOL:** FDC> * [CLICK HERE FOR CHART!](http://elite.finviz.com/chart.ashx?)""")

    doc = nlp(in_text)
    text, n, tick = norm_doc(doc)

    assert not hasNumbers(text)

    expected = {'rf', 'csx', 'bbt', 'fdc', 'ag', 'cbsh', 'mtb', 'snv', 'nbev', 'axp', 'frc', 'ozk', 'plab', 'c', 'ms',
                'key', 'apple', 'sasr', 'homb', 'kndi', 'dis', 'qcom', 'sjr', 'gs', 'jwn', 'cmg', 'shop', 'ntnx', 'schw',
                'bac', 'xlf', 'fast', 'ugaz', 'jbht', 'vfc', 'sti', 'blackrock', 'fult', 'vhc', 'ual', 'efii', 'jpmorgan',
                'dal', 'snapchat', 'hafc', 'nly', 'pcg', 'prgs', 'fisv', 'wns', 'unh', 'pnfp', 'mbot', 'netflix', 'pte',
                'plxs', 'aa', 'microsoft', 'kmi', 'wfc', 'pbct', 'ko', 'slb', 'pnc', 'cma', 'bk', 'team', 'usb', 'info'}

    assert expected == tick


def test_4():
    in_text = """> **Blackstone** – The private-equity firm posted quarterly economic net loss of 2 cents per share, 
    compared to estimates of a breakeven quarter. Revenue was well above estimates, however, and CEO Stephen 
    Schwarzman said nearly all of Blackstone's flagship strategies beat their relevant benchmarks in 2018. 
    Distributable net income also topped Wall Street forecasts.> #**STOCK SYMBOL:** BX> * [CLICK HERE FOR CHART!](
    http://elite.finviz.com/chart.ashx?t=BX&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,
    macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](
    http://data.cnbc.com/quotes/BX)**)*****> **Hershey** – The chocolate maker missed estimates by a penny a share, 
    with adjusted quarterly profit of $1.26 per share. Revenue was also shy of estimates. Hershey saw sales increases 
    in recently acquired snack brands, but that was offset by a drop in North American chocolate sales.> #**STOCK 
    SYMBOL:** HSY> * [CLICK HERE FOR CHART!](http://elite.finviz.com/chart.ashx?t=HSY&ty=c&ta=st_c,sch_200p,sma_50,
    sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE 
    STOCK QUOTE!](http://data.cnbc.com/quotes/HSY)**)*****> **UPS** – The delivery service earned an adjusted $1.94 
    per share for the fourth quarter, 4 cents a share above estimates. Revenue fell short of forecasts amid global 
    trade turbulence, but higher fees helped bottom line results.> #**STOCK SYMBOL:** UPS> * [CLICK HERE FOR CHART!](
    http://elite.finviz.com/chart.ashx?t=UPS&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,
    macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](
    http://data.cnbc.com/quotes/UPS)**)*****> **Microsoft** – Microsoft reported adjusted quarterly profit of $1.10 
    per share, beating consensus estimates by a penny a share. Revenue came in slightly short of forecasts, however, 
    despite a gain in its cloud-computing business as several other product areas saw slower growth.> #**STOCK 
    SYMBOL:** MSFT> * [CLICK HERE FOR CHART!](http://elite.finviz.com/chart.ashx?t=MSFT&ty=c&ta=st_c,sch_200p,sma_50,
    sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE 
    STOCK QUOTE!](http://data.cnbc.com/quotes/MSFT)**)*****> **Facebook** – Facebook beat estimates by 19 cents a 
    share, with quarterly profit of $2.38 per share. The social media giant's revenue also beat forecasts. The 
    results are lessening investor concerns about increased spending on privacy and security-related matters.> 
    #**STOCK SYMBOL:** FB> * [CLICK HERE FOR CHART!](http://elite.finviz.com/chart.ashx?t=FB&ty=c&ta=st_c,sch_200p,
    sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR 
    LIVE STOCK QUOTE!](http://data.cnbc.com/quotes/FB)**)*****> **Tesla** – Tesla earned an adjusted $1.93 per share 
    for its latest quarter, missing the $2.20 a share consensus estimate. The automaker's revenue beat Street 
    forecasts, however, and CEO Elon Musk expressed confidence that Tesla can be profitable every quarter. 
    Separately, the company announced the departure of chief financial officer Deepak Ahuja.> #**STOCK SYMBOL:** 
    TSLA> * [CLICK HERE FOR CHART!](http://elite.finviz.com/chart.ashx?t=TSLA&ty=c&ta=st_c,sch_200p,sma_50,sma_200,
    sma_20,sma_100,bb_20_2,rsi_b_14,macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK 
    QUOTE!](http://data.cnbc.com/quotes/TSLA)**)*****> **Tailgrass Energy** – Affiliates of Blackstone will acquired 
    a controlling stake in the energy infrastructure company for $3.3 billion in cash.> #**STOCK SYMBOL:** TGE> * [
    CLICK HERE FOR CHART!](http://elite.finviz.com/chart.ashx?t=TGE&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,
    sma_100,bb_20_2,rsi_b_14,macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](
    http://data.cnbc.com/quotes/TGE)**)*****> **Qualcomm** – Qualcomm reported adjusted quarterly profit of $1.20 per 
    share, 11 cents a share above estimates. The chipmaker's revenue fell short of Wall Street forecasts. Qualcomm 
    gave a forecast that was in line with analysts' estimates, soothing some concerns about weakness in the China 
    smartphone market.> #**STOCK SYMBOL:** QCOM> * [CLICK HERE FOR CHART!](
    http://elite.finviz.com/chart.ashx?t=QCOM&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,
    macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](
    http://data.cnbc.com/quotes/QCOM)**)*****> **Visa** – Visa beat estimates by 5 cents a share, with adjusted 
    quarterly profit of $1.30 per share. The payment network's revenue beat estimates, as well. Results were boosted 
    by an 11 percent increase in payment volume, and the company also announced an $8.5 billion stock buyback 
    program.> #**STOCK SYMBOL:** V> * [CLICK HERE FOR CHART!](http://elite.finviz.com/chart.ashx?t=V&ty=c&ta=st_c,
    sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK 
    HERE FOR LIVE STOCK QUOTE!](http://data.cnbc.com/quotes/V)**)*****> **PayPal** – PayPal reported adjusted 
    quarterly profit of 69 cents per share, 2 cents a share above estimates. The payment service's revenue was 
    essentially in line with forecasts, however PayPal gave a lower-than-expected revenue outlook for the current 
    quarter.> #**STOCK SYMBOL:** PYPL> * [CLICK HERE FOR CHART!](
    http://elite.finviz.com/chart.ashx?t=PYPL&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,
    macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](
    http://data.cnbc.com/quotes/PYPL)**)*****> **Mondelez International** – Mondelez matched Street forecasts with 
    adjusted quarterly profit of 63 cents per share, and the snack maker's revenue was in line with expectations, 
    as well. The company's sales fell in the latest quarter, but higher prices helped boost bottom line results.> 
    #**STOCK SYMBOL:** MDLZ> * [CLICK HERE FOR CHART!](http://elite.finviz.com/chart.ashx?t=MDLZ&ty=c&ta=st_c,
    sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK 
    HERE FOR LIVE STOCK QUOTE!](http://data.cnbc.com/quotes/MDLZ)**)*****> **Wynn Resorts** – Wynn earned an adjusted 
    $1.06 per share for its latest quarter, missing the consensus estimate of $1.35 a share. The casino operator's 
    revenue came in above Wall Street forecasts.> #**STOCK SYMBOL:** WYNN> * [CLICK HERE FOR CHART!](
    http://elite.finviz.com/chart.ashx?t=WYNN&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,
    macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](
    http://data.cnbc.com/quotes/WYNN)**)*****> **Unilever** – The consumer products giant reported 
    weaker-than-expected fourth-quarter results and warned of a challenging 2019, due to tougher competition in the 
    North American market.> #**STOCK SYMBOL:** UL> * [CLICK HERE FOR CHART!](
    http://elite.finviz.com/chart.ashx?t=UL&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,
    macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](
    http://data.cnbc.com/quotes/UL)**)*****> **General Motors** –GM temporarily suspended production at 11 Michigan 
    plants and its Warren Tech Center. The move comes after a local utility requested that users conserve natural gas 
    during the extreme cold snap.> #**STOCK SYMBOL:** GM> * [CLICK HERE FOR CHART!](
    http://elite.finviz.com/chart.ashx?t=GM&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,
    macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](
    http://data.cnbc.com/quotes/GM)**)*****> **United Natural Foods** – United Natural sued Goldman Sachs and Bank of 
    America/Merrill Lynch. The food distributor claimed the investment banks put their own financial interests ahead 
    of United Natural's when advising it on the acquisition of Supervalu last year. A Goldman spokeswoman said the 
    suit has no merit.> #**STOCK SYMBOL:** UNFI> * [CLICK HERE FOR CHART!](
    http://elite.finviz.com/chart.ashx?t=UNFI&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,sma_100,bb_20_2,rsi_b_14,
    macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](
    http://data.cnbc.com/quotes/UNFI)**)*****> **UnitedHealth Group** – The health insurer is suing to stop former 
    executive David Smith from joining the new joint health care venture formed by Amazon, Berkshire Hathaway, 
    and JPMorgan Chase. UnitedHealth claims the move violates Smith's noncompete agreement.> #**STOCK SYMBOL:** UNH> 
    * [CLICK HERE FOR CHART!](http://elite.finviz.com/chart.ashx?t=UNH&ty=c&ta=st_c,sch_200p,sma_50,sma_200,sma_20,
    sma_100,bb_20_2,rsi_b_14,macd_b_12_26_9,stofu_b_14_3_3&p=d&s=l)> ######(**[CLICK HERE FOR LIVE STOCK QUOTE!](
    http://data.cnbc.com/quotes/UNH)**)*****#**DISCUSS!**What is on everyone's radar for today's trading day ahead 
    here at r/wallstreetbets?*****# **I hope you all have an excellent trading day ahead today on this Thursday, 
    January 31st, 2019! :)** """
    text, n, tick = process_t(in_text)

    # F is missing
    assert {'tge', 'unfi', 'microsoft', 'pypl', 'amazon', 'mdlz', 'snapchat', 'facebook', 'hsy', 'tesla', 'ups',
            'berkshire', 'unh', 'gm', 'bx', 'v', 'ul', 'jpmorgan', 'wynn', 'qcom'} == tick
    assert not hasNumbers(text)


def test_unmark():
    in_text = norm(
        """ARKG holds stock that are so small part (<<10%) of the stock market.  And the fund is up 144% from a year ago. If you want to hold this, should not be more than 10% of your portfolio. risk is too concentrated.\n\nSee the example of ICLN - iShares Global Clean Energy ETF. This was $50 back in 2008 and has never seen those highs. Genomics and Clean energy could be the future - but those funds/stocks may not perform as well as you expect them to.\n\n|Fund|today|1 year low|% up in a year|% all time high|\n|:-|:-|:-|:-|:-|\n|ARKG|$90|$24|**144%**|***-22%***|\n|ICLN|$24|$8|**83%**|***-52% lower from 2008***|\n|SP500 (SPY)|||**21.9%**|***-1.3%***|""")

    doc = nlp(in_text)
    text, n, tick = norm_doc(doc)
    assert not hasNumbers(text.replace('sp500', ''))

    in_text = "That's awesome. I really felt bad about it today when I checked my portfolio. Hate when I give advice and it turns to shit the next day. \n\nOn my end, the downturn is highly unfortunate timing. Just moved my portfolio from Chase to TDAmeritrade, and my stocks are all frozen until next Monday. Guess I'm along for the [buttfuck]ride\n\nEdit: Those assholes at Chase even canceled my Stop Limit order (on the money frozen in their custody) that I placed on my 8 Tesla stocks if they dropped below $450. Called to see if they'd honor the order since it was placed pre-transfer, and they basically told me to get fucked."
    text, _, _ = process_t(in_text)
    assert not hasNumbers(text)


    in_text = """**Bid**$3.XX × 100 **Ask**$12.XX × 20**Mark**$8.XX
    **Previous Close**$1.XX
    **High**$XX **Low**$6.XX
    **Volume 20**
    **Open Interest**4**Implied Volatility**61.35%
    The Greeks
    **Delta**0.5040**Gamma**0.0186**Theta**\-0.3121**Vega**0.1395**Rho**0.0314"""

    text, n, tick = process_t(in_text)
    assert not hasNumbers(text)


def test_currency():
    in_text = """Because I’m not sure about the law. The declaration form question is:\n\n> AUD$10,000 or """
    text, _, _ = process_t(in_text)
    assert not hasNumbers(text)

    in_text = html.unescape("""**Wednesday (06/03/20)**\n\nStock closed @ $6.86\n\n\\+26¢ (+3.94%)\n\n&#x200B;\n\n**Thursday (
    06/04/20)**\n\nStock closed @ $6.75\n\n\\-11¢ (-1.60%)\n\n&#x200B;\n\n**Friday (06/05/20)**\n\nStock closed @ 
    $6.84\n\n\\+9¢ (+1.33%)\n\n&#x200B;\n\n**Up 40¢ for the week.** #[Yes Bank crisis: RBI caps withdrawal at ₹50,000, people queue up outside ATMs](
    https://www.youtube.com/watch?v=ikNvvYuIi3M)\n\n[Bitcoin song of the week](
    https://www.youtube.com/watch?v=GgnClrx8N2k) to all the Banksters, that\'s not Heart Burn it\'s Honey Badger. 
    Option is a contract (1) to buy or sell the stock (100) at a given price (Strike) at a given date (
    Expiration) Depending on the volatility and how near or far out the date or price is makes a big difference on 
    the premium you pay, in my case I paid .26 a contract so .26x100 = $26 for a $1 strike price while the stock was 
    at $1.60 but it was falling and volatile so that explains why the premium was so high. So my experation date is 
    5/1 (May 1st) I need the stock to close below $1 on that day to be in the money but remember I paid .26 so to 
    break even I need it to be $1.00 - .26c = .74 to be even. So lets say it closes at .30 so my 25 contracts I 
    bought at $26 ($650) would be worth 2500 shares x .70c (difference from strike) = $1750.00. Now this would be a 
    real good outcome but remember if they keep it over $1 I lose it all. """)
    text, _, _ = process_t(in_text)
    assert not hasNumbers(text.replace('1st', ''))


def process_t(in_text):
    doc = nlp(norm(in_text))
    return norm_doc(doc)


def test_snp():
    in_text = "Actually, Berkshire has outperformed the S&P/SPY. From 1965 to present, there is an average annual return " \
              "of 20.5%. This is a bit more than double the S&P's return, depending on how you deal with inflation.  " \
              "Spy tracks the S&P.\n\nYou can't physically invest in the S&P, S&P500 spy is how you invest to closely match " \
              "it. , and also P/Es P/B P/P/E " \
              "S&P/CS HPI Composite [2/3 Volatility]"
    text, n, tick = process_t(in_text)
    assert ' p ' not in text


def test_5():
    in_text = """\n\nHeron Therapeutics (NASDAQ: $HRTX) is a \\~$1.95B market cap biotech company waiting on an FDA 
    decision this week for their non-opioid postoperative pain management drug HTX-011. $HRTX received Fast Track, 
    Breakthrough, and Priority Review designations for HTX-011, underscoring the critical need for effective 
    non-opioid painkillers in the wake of the ongoing opioid epidemic, which was fueled historically in part by 
    post-surgery opioid prescriptions. HTX-011 is an elegant and creative solution seeking to provide a better option 
    to patients post-surgery and minimize the need for opioids. HTX-011 is a proprietary extended release combination 
    formulation of [bupivacaine](https://en.wikipedia.org/wiki/Bupivacaine) and [meloxicam](
    https://en.wikipedia.org/wiki/Meloxicam)\\- details about this intriguing synergistic mechanism of action are 
    included below. Exparel, a minimally differentiated bupivacaine product approved for post-surgical analgesia (
    pain relief), earned >$400M in sales in 2019. Therefore we believe peak sales in the $600 - 1000M range are 
    achievable for HTX-011 based on the potential for clinical differentiation with substantial further upside 
    feasible pending supportive real-world data.\n\n**Key Takeaways**\n\n* We are bullish on the anticipated FDA 
    decision this week and expect to see HTX-011 approved (>90% probability of success), with some serious upside 
    depending on the exact labeled indication.\n* Based on prior stock performance and consensus analyst price 
    targets in the $35 - 41.50 range, we believe that an approval this week should drive $HRTX near to or above $30, 
    at which point we would look to exit our position given concerns we have with launching a product like this in a 
    COVID environment.\n\n*See below for further details:*\n\n**Regulatory Background**$HRTX initially filed their 
    NDA for HTX-011 in late 2018, but received a [Complete Response Letter](
    https://herontherapeutics.gcs-web.com/news-releases/news-release-details/heron-therapeutics-receives-complete
    -response-letter-htx-011) (CRL) in April 2019 due to Chemistry, Manufacturing, and Controls (CMC) concerns. $HRTX 
    worked with their contract manufacturer and resubmitted the NDA in October 2019. $HRTX reported in February 2020 
    that the manufacturing site had been reinspected and the FDA inspector had recommended approval of the site, 
    potentially finally clearing the runway to an overdue FDA decision by the June 26th, 2020 PDUFA date (a 
    three-month delay from the original March PDUFA date). These non-clinical factors are the hardest for us to 
    predict, but we are reassured by the successful reinspection and the fact that FDA did not note any clinical 
    deficiencies in their application.  \n**Unique Product Creatively Building on Existing Clinical Options**HTX-011 
    is an extended release formulation of bupivacaine and meloxicam that is applied directly into the surgical 
    incision site without a needle.\n\n* [Bupivacaine](https://en.wikipedia.org/wiki/Bupivacaine) (like other -caine 
    drugs, e.g., lidocaine) is a commonly used injectable nerve blocker to decrease the sensation of pain, 
    while [meloxicam](https://en.wikipedia.org/wiki/Meloxicam) is a nonsteroidal anti-inflammatory drug (NSAID).\n* 
    Both drugs are generically available, though HTX-011 is a unique product using a [proprietary polymer](
    https://www.herontx.com/our-technologies) that enables extended local release, lengthening the effect time.\n\nWe 
    think this is an exciting mechanistic approach for a number of reasons:\n\n* Both component molecules are 
    well-established and effective\n* Inflammation creates a more acidic environment- the anti-inflammatory effects 
    of meloxicam could mitigate this and improve bupivacaine diffusion, allowing it to exert its effect more 
    efficiently.\n* Non-needle applicator could be more convenient and user-friendly than performing multiple 
    injections, as is required with bupivacaine.\n* Local administration of meloxicam (rather than intravenous) could 
    potentially minimize systemic effects / concerns with its use.\n\n**Differentiated Data With Potential For 
    “Opioid-sparing” Language to be Included in Label**HTX-011 demonstrated a superior reduction in pain intensity 
    versus injected bupivacaine across two pivotal P3 trials in patients post-bunionectomy and post-herniorrhaphy 
    procedures, respectively. This was measured by plotting patient-assessed pain intensity on a scale from 1 - 10 at 
    various time points up to 72 hours post-surgery, and then measuring the “area under the curve” (AUC): a lower AUC 
    indicates lower pain intensity over that time period.\n\n* Beyond a statistically significant lower AUC over the 
    entire 72 hour period, HTX-011 patients also demonstrated a meaningfully lower pain score at 12, 24, 36, 
    and 48 hours post-surgery, with the scores beyond that starting to even out.\n* This suggests that over the first 
    48 hours at least HTX-011 measurably reduces the patient experience of pain.\n\nWe were also excited to see that 
    HTX-011 significantly reduced the total opioid medication use over that same 72 hour window:\n\n* For the 
    bunionectomy trial, 28.7% of HTC-011 patients were completely opioid-free versus 11% of bupivacaine-treated 
    patients.\n* In the post-herniorrhaphy trial, 51.2% of HTX-011 patients versus 40.1% of bupivacaine-treated 
    patients were opioid-free.\n* Optimistically, we would hope that this language would make its way into the 
    FDA-approved label, which would be a huge boost for $HRTX as they could then market the product with the claim 
    that it can reduce the need for opioids.\n\nWe have some concerns with the dosing used in the trials, 
    with the HTX-011 arms consistently containing a higher concentration of bupivacaine in the HTX-011 combination 
    than the amount of bupivacaine used for the control arms, which could be part of the reason for the superior pain 
    relief of the HTX-011. However we do not think the FDA will get too hung up on this as HTX-011 also resoundly 
    beat the placebo arm. Nonetheless we expect hospitals and other healthcare providers to test HTX-011 in the 
    real-world versus comparable bupivacaine doses before adopting the product widely.  \nFor context, Exparel, 
    an extended release formulation of bupivacaine was approved in 2011 on the basis of trial demonstrating superior 
    pain relief to placebo with no impact on opioid use: real-world studies have shown that Exparel is not much if at 
    all better than generic bupivacaine, so the strong data for HTX-011 versus bupivacaine sets it up to be perceived 
    as a differentiated clinical offering.\n\n**Other Considerations**$HRTX also has two already approved products in 
    Sustol and Cinvanti, both for prevention of chemotherapy-induced nausea or vomiting ([CINV](
    https://en.wikipedia.org/wiki/Chemotherapy-induced_nausea_and_vomiting)). We did not consider these products to 
    contribute meaningful upside as both products are facing challenging commercial environments due to 
    genericization of key competitors. However, having these products in their portfolio means $HRTX already has a 
    commercial infrastructure targeting hospitals, which should offer some synergies with the HTX-011 potential 
    launch.\n\n\\*\\*Disclosure:\\*\\*We own shares of Heron Therapeutics. This article expresses our own opinions, 
    not Heron Therapeutics’ or any other party’s opinion. We are not receiving compensation for this report. We do 
    not have a business relationship with the company mentioned in this report. """
    text, n, tick = process_t(in_text)
    assert {'cinv', 'hrtx'} == tick


def test_number():
    in_text = "They do generally, 2017-2018 median real (which mean adjusted to inflation) wages are increasing by a 0.9% with a ±1.06 error margin all households combines ([Source](https://www.census.gov/data/tables/2019/demo/income-poverty/p60-266.html), Table A-1). Over decades, median real earnings for workers are [generally going up](https://fred.stlouisfed.org/series/LES1252881600Q) (slowly).\n\nThis of course doesn't address the rising costs of certain spending categories like healthcare and the many inequalities poor people face... but by sheer numbers they are slowly growing."
    text, n, tick = process_t(in_text)
    assert not hasNumbers(text)


# test_1()
# test_2()
# test_3()
# test_4()
