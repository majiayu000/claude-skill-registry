---
name: nlb
description: check loans and search resources from the National Library Board of Singapore
homepage: https://www.nlb.gov.sg
metadata:
  { "clawdbot": { "emoji": "📚", "requires": { "bins": [] }, "install": [] } }
---

# NLB Skill

## Login to NLB

1. Open https://signin.nlb.gov.sg/authenticate/login
2. Use user myLibrary username and password to login

## Check Loans(requires login)

1. Open https://www.nlb.gov.sg/mylibrary/loans
2. Check "Current" Tab to see borrowed items and due dates
3. Check "Overdue" Tab to see past borrowed items

## Check Recommendations(requires login)

1. Open https://www.nlb.gov.sg/mylibrary/Home

## Search Resources

1. URL Encode the search query
2. Open search result page: https://catalogue.nlb.gov.sg/search?query={url_encoded_query}
   Optional URL parameter filters:
   - &universalLimiterIds=at_library (to filter to only items available at libraries)
   - &pageNum=0 (to specify page number, starting from 0)
   - &viewType=grid (to view results in grid format)
   - &materialTypeIds=1 (to filter to books only)
   - &collectionIds={collection_ids} (to filter by specific collections, see below for details)
   - &locationIds={location_ids} (to filter by specific libraries, see below for details)
   - languageIds={language_ids} (to filter by specific languages, chi: Chinese, eng: English, mal: Malay, tam: Tamil)

### Collection Id Mappings:
| Collection Name                      | Collection Id |
| ------------------------------------ | ------------- |
| Early Literacy 4-6                   | 7             |
| Junior Picture Book                  | 11            |
| Junior                               | 9             |
| Early Literacy Accessible Collection | 55            |
| Junior Simple Fiction                | 12            |
| Junior Accessible Collection         | 8             |
| Adult                                | 3             |

### Location Id Mappings:
| Library Name      | Location ID |
| ----------------- | ----------- |
| Toa Payoh Library | 23          |
| Bishan Library    | 6           |
| Central Library   | 29          |


### Example

For search query "BookLife readers", filtering to items book only, available at Toa Payoh Library, in Junior Picture Book and Junior collections, viewing first page in grid format:
https://catalogue.nlb.gov.sg/search?query=BookLife%20readers&pageNum=0&locationIds=23&universalLimiterIds=at_library&collectionIds=11,9,7&viewType=grid&materialTypeIds=1

## Open Search Crad Page
1. Click the rearch result link to open the search result page in browser
Search Card Page Example:
https://catalogue.nlb.gov.sg/search/card?id=127ebe36-bad7-566c-8d81-3a32379254ad&entityType=FormatGroup

