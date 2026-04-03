"""
delete_opportunities.py
Deletes opportunities created by Barry's import on March 25, 2026.
Reads CLOSE_API_KEY and DRY_RUN from environment variables (set via GitHub secrets/inputs).
"""

import os
import csv
import time
import requests
from datetime import datetime, timezone

API_KEY      = os.environ["CLOSE_API_KEY"]
DRY_RUN      = os.environ.get("DRY_RUN", "true").lower() == "true"
DATE_START   = "2026-03-25T00:00:00+00:00"
DATE_END     = "2026-03-26T00:00:00+00:00"
LOG_FILE     = "opportunity_deletion_log.txt"
BASE_URL     = "https://api.close.com/api/v1"

COMPANIES = ["12 Oaks Senior Living","29th Street Capital","Accura HealthCare","Accushield","Achieve Accreditation","Acts Retirement-Life Communities, Inc.","ACTS Retirement-Life Communities, Inc.","Adams Health Network","AdviniaCare","Aegis Living","Agemark Senior Living","AgeWell Solvere Living","AlcoreSenior","Aline","Allaire Health Services","Allegro Senior Living, LLC","Allure Lifestyle Communities","Alta Senior Living","Alumus","American House Senior Living Communities","ANF Group Inc","ANF Group, Inc.","Anthem Memory Care","Aperto Property Management, Inc.","Aramark","ARAMARK","ARAMARK Higher Education","ArchCare","Argentum","Arrow Senior Living Management","Artis Senior Living","Asbury Communities, Inc.","Ascension","Ascension Living","Ashford Senior Living","Aspire Senior Living","Atlas Healthcare Group","Atlas Senior Living","Atria Senior Living","Aviva Senior Living","Azura Memory Care / Azura Living","B2K Development","Bainbridge Senior Living","BaneCare Management","Baptist Life Communities","Baruch Senior Ministries","Benchmark Assisted Living","Benchmark Senior Living","Benedictine","Bethesda Health Group","Beztak","Blue Skies of Texas","Brandywine Living","Bridge Senior Living","Bridgeway Senior Healthcare","Brightview Senior Living","Brio Living Services","Brookdale","Brookdale Senior Living","Buckner International","Buckner Retirement Services","Buckner Retirement Services, Inc.","Capri Communities","Caring Place Healthcare Group","Caring Places Management","Carle Health","Cascade Living Group","Cascade Senior Living Services","Cascadia Senior Living & Fieldstone Communities","Catholic Eldercare","Catholic Health Services","CCL Hospitality Group","Cedarbrook Senior Living","Certus Healthcare","CERTUS Senior Living","Chapters Management Group","Charles E. Smith Life Communities","Charter Senior Living","Christian Care / Fellowship Square","Christian Care Communities & Services","Christian Community Homes and Services, Inc","Ciel Senior Living","Civitas Senior Living","CJE SeniorLife","Clearwater Living","Cogir Senior Living","Colavria Hospitality","Colliers International","CommCare Corporation","Common Sail Investment Group","Commonwealth Senior Living","CommuniCare Health Services","Community Wellness Partners","Compass Senior Living","Consonus Healthcare","Consulate Health Care","Cornerstone Management Services","Coterie Senior Living","Covenant Care","Covenant Health (MA)","Covenant Living Communities and Services","Creative Solutions In HealthCare","CRISTA Senior Living","CSJ INITIATIVES, INC.","Cuhaci Peterson","Culinesse, LLC","Curana Health","Curtis Squire, Inc.","Danbury Senior Living","Denton Floyd Real Estate Group","DePaul","DiningRD","DiningRD | Health Technologies, Inc.","Direct Supply","Discovery management group","Discovery Senior Living","Distinctive Living","Diversicare Healthcare Services Inc.","DMK Development Group","Dominion Group","Ecumen","Eden Senior Care","Eduro Healthcare","ElderSpan Management, LLC","Elderwood","Elegance Senior Living","Elior","Elior North America","Elysian Senior Homes","Encore Healthcare Services","Episcopal Homes of Minnesota","Episcopal Retirement Services","Episcopal SeniorLife Communities","Epworth Villa","Eskaton","EUA","Eventide Senior Living Communities","Evergreen Management","Everlan By Dominion","EveryAge","Fellowship Senior Living","FellowshipLIFE","Fore Property","Forefront Living","Foresite Healthcare","Formation Capital","Franciscan Ministries","Franciscan Ministries Sponsored by the Franciscan Sisters of Chicago","Frontier Management, LLC","Galerie Living","Gardant","Gardant Management Solutions","Generations Healthcare","Generations Healthcare Management","GentleBrook","George Gekakis Inc","Gifford","Glencoe Regional Health","Goldrich Kest","Goodwin Living","Graceworks Lutheran Services","Grand Living","Great Lakes Management","Great Lakes Management Company","Greencroft Communities","Greystone Communities","Harmony Senior Services","Harrison Senior Living","Hartford HealthCare","Havenwood Heritage Heights","HCF Management, Inc.","Health Dimensions Group","HealthPRO Heritage","Heritage Communities","Heritage Community of Kalamazoo","Heritage Operations Group, LLC","HHS","HHS - Hospitality Services","HHS, LLC","HMG Healthcare","Holy Redeemer Health System","Homewood Living Ministries","Immanuel","Infinite Services Inc","Inspirit Senior Living","IntegraCare Corporation","Integrated Real Estate Group","Integrated Real Estate Group (Integrated Senior Lifestyles)","Jaybird Senior Living","JES Holdings, LLC","Jewish Association on Aging","Jewish Senior Life of Metropolitan Detroit","Judson Senior Living","Juniper Communities, llc","Kadima Healthcare","KBE Building Corporation","Keystone Senior Management Services, Inc.","Kingston HealthCare","Kingston Healthcare","Kintura","Kintura (formerly The Well\u2022Spring Group)","Kisco Senior Living","Koelsch Communities","Koru Health LLC","La Posada Green Valley, AZ","LCB Senior Living, LLC","LeadingAge","Legacy Health Services","Legend Senior Living","Liberty Healthcare Management","Liberty Lutheran","Liberty Senior Living","Life Enriching Communities","Lifespace Communities, Inc.","Lifespark","Lifesprk","link-age","LionStone Care","Liv Communities LLC","Living Branches","Longview Senior Housing","Lorien Health Services","Los Angeles Jewish Health","Lutheran Life Communities","Lutheran Life Villages","Lutheran Services Carolinas","Lutheran Social Services of Central Ohio","Luthercare","Madison Healthcare Services","Maine Veterans\u200b Homes","Majestic Care","Maplewood Senior Living","Marquis Companies","Masonicare","Mather","MBK Real Estate Companies","MBK Senior Living","MedCore Partners","Medical Assets Holding Company","Merrill Gardens","Miami Jewish Health","Miami Jewish Health Systems","Midwest Health, Inc.","Miravida Living","Monarch Communities","Monarch Healthcare Management","Moorings Park","Moorings Park Communities","Morning Pointe Senior Living","MorningStar Senior Living","MorseLife Health System, Inc.","National Church Residences","National HealthCare Corporation (NHC)","New Perspective Senior Living","Nexcare Health Systems","NexCare WellBridge Senior Living","NexCore Group","NEXDINE Hospitality","Nexion Health","North Shore Health","North Shore Healthcare, LLC","Northbridge Companies","NuCare Senior Living","Oakdale Seniors Alliance","Oakmont Senior Living","Omega Senior Living","Optalis Health & Rehabilitation Centers","Otterbein SeniorLife","Ovation Communities","Pacific Retirement Services","PACS","PACS | Providence Administrative Consulting Services","Palm Garden","Paradise Valley Estates","Paragon Senior Living","Paramount Health Resources, Inc.","Parc Communities","Park Street Senior Living","Peabody Companies","Peabody Properties, Inc.","Peak Resources, Inc","Pennant","Pennrose","Pennybyrn","Phoenix Senior Living","Phoenix3 Collective","Phoenix3 Holdings","PK Management, LLC","Plante Moran","PMMA (Presbyterian Manors of Mid-America)","Presbyterian Homes & Services","Presbyterian Homes of Athens","Presbyterian Homes of Georgia","Presbyterian Homes, Inc","Presbyterian Living","Presbyterian Senior Living","Presbyterian SeniorCare Network","Primrose Retirement Communities, LLC","Progressive Quality Care","ProMedica","Proveer Senior Living","Quality Life Services","Radiant Senior Living","Rakhma, Inc","Rees Associates","Rennes Group","Resthaven (Holland, Michigan)","RESTORATION SENIOR LIVING, LLC","Retirement Unlimited Inc","Revel Communities","RiverWoods","Rocky Mountain Care","Royal Health Group","RSR SENIOR RESIDENCES","Saber Healthcare Group","SageLife","Sagora Senior Living","SALMON Health and Retirement","Samaritan Bethany, Inc.","Sapphire Health Services, LLC","Savant Senior Living","Sayre Christian Village","ScionHealth","Seabury","Senior Living Communities, LLC","Senior Living Hospitality","Senior Solutions Management Group","Sequoia Living","Shepherd Of The Valley Lutheran Retirement Services, Inc.","Signature HealthCARE","Signature Healthcare","Silver Birch Living","Silver Companies","Silverado","Simpson","Sisters of St Francis of Assisi, Inc.","Sodalis Senior Living","Sodexo","SODEXO (former SODEXHO)","Sodexo Corporate Services","Sodexo Services","Solera Senior Living","Spectrum human services","SpiriTrust Lutheran","Sprenger Health Care Systems","Spring Hills","Spring Oak Senior Living","Springpoint Senior Living","SR Companies","SRI Management, LLC","St. Ann's Community","St. Paul's Senior Services","Steadfast Companies","StoryPoint","Suite Living Senior Care","Sun Health","Sunnyside Communities","Sunrise Senior Living","Sunset Senior Communities","Symphony Care Network","Tarantino Properties, Inc.","Terrace Glen Village","The Arbor Company","The Aspenwood Company","The Bristal Assisted Living","The Commonwealth Companies","The DePaul Group","The Geneva Suites","The Glenridge On Palmer Ranch, Inc.","The Kensington - Assisted Living","The Orchards Michigan","The Palace Group","The Ridge Senior Living","The Schroer Group","The Springs Living, LLC","The Waters Senior Living","The William James Group","The Wirt-Rivette Group","The Wolff Company","Thornapple Manor","Three Pillars Senior Living Communities","Three Pillars Senior Living Communities (Independent, Assisted, Memory, Skilled, Rehab, & Wellness)","ThriveMore","TMC: Therapy Management Corporation","Touchmark","Transforming Age","Transitions Healthcare, LLC","Trinity Healthcare","True Connection Communities","Trustwell Living, LLC","UMC - Abundant Life for Seniors","United Properties","USR Engage","Vantage Senior Care","Ventana By Buckner","VHCA-VCAL","Vi","Vi at Palo Alto  (formerly Classic Residence by Hyatt)","Vi at Silverstone formerly known as Classic Residence by Hyatt","Via Elegante Assisted Living & Memory Care","Victory Housing, Inc.","Vista Prairie Communities","Vivie","Wallick","Wallick Communities","Watercrest Senior Living Group","Watermark Retirement Communities","WellQuest Living","Wendover Housing Partners","Wesley","Western Home Communities","Westminster Communities of Florida","Westmont Living, Inc.","Willow Ridge Senior Living","Wingate Companies","Wingate Living","Woodbury Corporation","YourLife Senior Living"]

session = requests.Session()
session.auth = (API_KEY, "")

def api_get(path):
    r = session.get(f"{BASE_URL}{path}")
    r.raise_for_status()
    return r.json()

def api_delete(path):
    r = session.delete(f"{BASE_URL}{path}")
    r.raise_for_status()

def main():
    mode = "DRY RUN" if DRY_RUN else "LIVE DELETE"
    print(f"\n{'='*60}")
    print(f"  {mode}")
    print(f"  Companies: {len(COMPANIES)}")
    print(f"  Date range: {DATE_START} → {DATE_END}")
    print(f"{'='*60}\n")

    log_lines = []
    processed = found = deleted = skipped = errors = 0

    for i, company in enumerate(COMPANIES, 1):
        print(f"[{i}/{len(COMPANIES)}] {company}", end=" ... ", flush=True)

        # Search for lead
        try:
            res = api_get(f'/lead/?query={requests.utils.quote(f"name:\"{company}\"")}&_limit=3')
            leads = res.get("data", [])
        except Exception as e:
            print(f"SEARCH ERROR: {e}")
            errors += 1
            log_lines.append(f"SEARCH ERROR | {company} | {e}")
            time.sleep(0.3)
            continue

        if not leads:
            print("not found")
            skipped += 1
            time.sleep(0.1)
            continue

        lead_id = leads[0]["id"]

        # Find opportunities in date range
        try:
            res = api_get(
                f"/opportunity/?lead_id={lead_id}"
                f"&date_created__gte={requests.utils.quote(DATE_START)}"
                f"&date_created__lt={requests.utils.quote(DATE_END)}"
                f"&_limit=50"
            )
            opps = res.get("data", [])
        except Exception as e:
            print(f"OPP FETCH ERROR: {e}")
            errors += 1
            log_lines.append(f"OPP FETCH ERROR | {company} | {lead_id} | {e}")
            time.sleep(0.3)
            continue

        if not opps:
            print("no opps in range")
            skipped += 1
            time.sleep(0.1)
            continue

        found += len(opps)
        print(f"{len(opps)} opp(s) found")

        for opp in opps:
            label = opp.get("note") or opp.get("status_label") or opp["id"]
            if DRY_RUN:
                print(f"  → WOULD DELETE | {opp['id']} | {label}")
                log_lines.append(f"WOULD DELETE | {company} | {opp['id']} | {label}")
            else:
                try:
                    api_delete(f"/opportunity/{opp['id']}/")
                    deleted += 1
                    print(f"  ✓ DELETED | {opp['id']} | {label}")
                    log_lines.append(f"DELETED | {company} | {opp['id']} | {label}")
                    time.sleep(0.15)
                except Exception as e:
                    print(f"  ✗ DELETE ERROR | {opp['id']} | {e}")
                    errors += 1
                    log_lines.append(f"DELETE ERROR | {company} | {opp['id']} | {e}")

        time.sleep(0.25)
        processed += 1

    # Summary
    print(f"\n{'='*60}")
    print(f"  COMPLETE — {mode}")
    print(f"  Processed:  {processed}")
    print(f"  {'Found' if DRY_RUN else 'Deleted'}:    {found if DRY_RUN else deleted}")
    print(f"  Skipped:    {skipped}")
    print(f"  Errors:     {errors}")
    print(f"{'='*60}\n")

    with open(LOG_FILE, "w") as f:
        f.write(f"Run at: {datetime.now(timezone.utc).isoformat()}\n")
        f.write(f"Mode: {mode}\n")
        f.write(f"Date range: {DATE_START} → {DATE_END}\n")
        f.write(f"Companies: {len(COMPANIES)}\n")
        f.write(f"Opps {'found' if DRY_RUN else 'deleted'}: {found if DRY_RUN else deleted}\n")
        f.write(f"Errors: {errors}\n\n")
        f.write("\n".join(log_lines))

    print(f"Log saved to {LOG_FILE}")

    # Fail the action if there were errors so it's visible in GitHub
    if errors > 0:
        raise SystemExit(f"{errors} error(s) encountered — check log artifact.")

if __name__ == "__main__":
    main()
