"""
delete_opportunities.py

Two-pass cleanup for Modern Amenities Close CRM:

PASS 1 — Barry's import fix
  Deletes opportunities on 418 Senior Living company leads
  that were created on March 25, 2026 (Barry's accidental import).

PASS 2 — Stephen Olivas owned opportunities
  Deletes ALL opportunities assigned to Stephen Olivas
  (user_5cZRqXu8kb4O1IeBVA98UMcMEhYZUhx1fnCHfSL0YMV), no date filter.

Reads CLOSE_API_KEY and DRY_RUN from environment variables.
"""

import os
import time
import requests
from datetime import datetime, timezone

API_KEY         = os.environ["CLOSE_API_KEY"]
DRY_RUN         = os.environ.get("DRY_RUN", "true").lower() == "true"
DATE_START      = "2026-03-25T00:00:00+00:00"
DATE_END        = "2026-03-26T00:00:00+00:00"
STEPHEN_USER_ID = "user_5cZRqXu8kb4O1IeBVA98UMcMEhYZUhx1fnCHfSL0YMV"
LOG_FILE        = "opportunity_deletion_log.txt"
BASE_URL        = "https://api.close.com/api/v1"

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

def process_opp(opp, label_prefix, log_lines):
    label = opp.get("note") or opp.get("status_label") or opp["id"]
    lead_name = opp.get("lead_name", opp.get("lead_id", "unknown lead"))
    if DRY_RUN:
        print(f"  → WOULD DELETE | {label_prefix} | {opp['id']} | {label}")
        log_lines.append(f"WOULD DELETE | {label_prefix} | {opp['id']} | {label} | lead: {lead_name}")
        return 1, 0, 0
    else:
        try:
            api_delete(f"/opportunity/{opp['id']}/")
            print(f"  ✓ DELETED | {label_prefix} | {opp['id']} | {label}")
            log_lines.append(f"DELETED | {label_prefix} | {opp['id']} | {label} | lead: {lead_name}")
            time.sleep(0.15)
            return 1, 1, 0
        except Exception as e:
            print(f"  ✗ ERROR | {opp['id']} | {e}")
            log_lines.append(f"ERROR | {label_prefix} | {opp['id']} | {e}")
            return 1, 0, 1


def pass1_barry_import(log_lines):
    print(f"\n{'─'*60}")
    print(f"  PASS 1 — Barry's Import (March 25, 2026)")
    print(f"  {len(COMPANIES)} companies | {DATE_START} → {DATE_END}")
    print(f"{'─'*60}\n")
    log_lines.append("=" * 60)
    log_lines.append("PASS 1 — Barry's Import (March 25 2026)")
    log_lines.append("=" * 60)

    processed = found = deleted = skipped = errors = 0

    for i, company in enumerate(COMPANIES, 1):
        print(f"[{i}/{len(COMPANIES)}] {company}", end=" ... ", flush=True)

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
            log_lines.append(f"OPP FETCH ERROR | {company} | {e}")
            time.sleep(0.3)
            continue

        if not opps:
            print("no opps in range")
            skipped += 1
            time.sleep(0.1)
            continue

        print(f"{len(opps)} opp(s)")
        for opp in opps:
            f, d, e = process_opp(opp, company, log_lines)
            found += f; deleted += d; errors += e

        time.sleep(0.25)
        processed += 1

    print(f"\n  Pass 1 done — {'found' if DRY_RUN else 'deleted'}: {found if DRY_RUN else deleted} | skipped: {skipped} | errors: {errors}")
    return found, deleted, errors


def pass2_stephen_opps(log_lines):
    print(f"\n{'─'*60}")
    print(f"  PASS 2 — All opportunities owned by Stephen Olivas")
    print(f"  No date filter — deletes everything assigned to this user")
    print(f"{'─'*60}\n")
    log_lines.append("")
    log_lines.append("=" * 60)
    log_lines.append("PASS 2 — All Stephen Olivas Opportunities (no date filter)")
    log_lines.append("=" * 60)

    found = deleted = errors = 0
    cursor = None
    page = 1

    while True:
        try:
            url = f"/opportunity/?user_id={STEPHEN_USER_ID}&_limit=100"
            if cursor:
                url += f"&_cursor={requests.utils.quote(cursor)}"
            res = api_get(url)
        except Exception as e:
            print(f"  FETCH ERROR (page {page}): {e}")
            errors += 1
            log_lines.append(f"FETCH ERROR page {page} | {e}")
            break

        opps = res.get("data", [])
        if not opps:
            print(f"  No more opportunities found.")
            break

        print(f"  Page {page} — {len(opps)} opportunities")
        for opp in opps:
            f, d, e = process_opp(opp, "Stephen Olivas", log_lines)
            found += f; deleted += d; errors += e

        cursor = res.get("cursor")
        if not cursor:
            break

        page += 1
        time.sleep(0.3)

    print(f"\n  Pass 2 done — {'found' if DRY_RUN else 'deleted'}: {found if DRY_RUN else deleted} | errors: {errors}")
    return found, deleted, errors


def main():
    mode = "DRY RUN" if DRY_RUN else "LIVE DELETE"
    print(f"\n{'='*60}")
    print(f"  {mode} — Modern Amenities Close CRM")
    print(f"{'='*60}")

    log_lines = [
        f"Run at: {datetime.now(timezone.utc).isoformat()}",
        f"Mode: {mode}",
        "",
    ]

    p1_found, p1_deleted, p1_errors = pass1_barry_import(log_lines)
    p2_found, p2_deleted, p2_errors = pass2_stephen_opps(log_lines)

    total_found   = p1_found   + p2_found
    total_deleted = p1_deleted + p2_deleted
    total_errors  = p1_errors  + p2_errors

    print(f"\n{'='*60}")
    print(f"  COMPLETE — {mode}")
    print(f"  Pass 1 (Barry's import):  {'found' if DRY_RUN else 'deleted'} {p1_found if DRY_RUN else p1_deleted}")
    print(f"  Pass 2 (Stephen's opps):  {'found' if DRY_RUN else 'deleted'} {p2_found if DRY_RUN else p2_deleted}")
    print(f"  Total:                    {total_found if DRY_RUN else total_deleted}")
    print(f"  Errors:                   {total_errors}")
    print(f"{'='*60}\n")

    log_lines += [
        "",
        "=" * 60,
        "SUMMARY",
        f"Pass 1 (Barry import)  — {'found' if DRY_RUN else 'deleted'}: {p1_found if DRY_RUN else p1_deleted}",
        f"Pass 2 (Stephen opps)  — {'found' if DRY_RUN else 'deleted'}: {p2_found if DRY_RUN else p2_deleted}",
        f"Total errors: {total_errors}",
    ]

    with open(LOG_FILE, "w") as f:
        f.write("\n".join(log_lines))
    print(f"Log saved to {LOG_FILE}")

    if total_errors > 0:
        raise SystemExit(f"{total_errors} error(s) encountered — check log artifact.")


if __name__ == "__main__":
    main()
