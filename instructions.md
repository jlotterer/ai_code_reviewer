Create Baseline Documents
1. SharePoint List Schemas 
   - export csv list with schema, store in ./sharepoint/lists
   - run prompt to review and create a RULES_SCHEMA.md file

2. Power Apps
   - go to apps
     - right click and select export
     - Open file, and extract app and flow json files
       - Flow: ./Microsoft.Flow/flows/b90dsk.../definition.json
       - App: ./Microsoft.PowerApps/apps/1145.../N46578...-document.msapp
          - /Src take all yaml files
          - /Resources / DataSources.json
          - Properties.json

3. Power Automate (if you can't download the Power App Zip file)
    - Use PA Extractor Flow


---

## SEQUENCE
  1. Requirements Review - are we building the right thing?
  2. Architecture Review - did we built it the right way?
  3. Consistency Review - Is the same business concept implemented consistently throughout the solution?
  4. Data Contract Review - Do all components agree on the structure of the data?
  5. PowerFx Review - Can the formulas be simplified, hardened, or optimized?
  6. Power Automate Review - runtime failures, expression issues, and flow design problems 
  7. Power App Review

---

## FILE STRUCTURE
/docs
  requirements.md
  architecture.md
  design-decisions.md

/app
  powerapp.json

/flows
  flow1.json
  flow2.json
  ...

/lists
  list1.csv (with schema)
  list2.csv
  ...

/config
  sharepoint-lists.md
  dataverse-schema.md
  environment-variables.md



=================================
SCHEMA PROMPT
=================================
NOTE TO USER: If you don't have list schemas already, have AI review the downloaded list CSVs and generate a schema for each in json and md format.
And create a SCHEMA_INDEX.md file and keep everything in a /schema subfolder

Either use extract_schemas.py to do this or have the agent do it.


=================================
INVENTORY PROMPT
=================================
Build an application inventory. 


=================================
MAIN PROMPT
=================================
You will be performing a detailed code review on a Power Apps solution with a Power Automate flow and SharePoint lists for data storage. We will perform this review in multiple phases: architecture, requirements, consistency, data contract, power app, power automate, and powerfx. Each phase is defined in a separate prompt .md file in review_prompts. See README.md for the review pattern and OUTPUT_CONTRACT.md for the required outputs. Implementation lives in app, flows, and lists. Requirements live in ./docs/requirements.md. Reports go under ./reports/2026-07-15/. Acknowledge the plan and wait for me to trigger each phase.


=================================
CHECK PROMPT
=================================
Do you have all of the files you need to perform this review?


=================================
REQUIREMENTS REVIEW
=================================
Using REQUIREMENTS_REVIEW.md, review the implementation under ./app and ./flows and ./lists against the requirements in ./docs/requirements.md. Write outputs to ./reports/2026-07-15/

INPUTS:
* Requirements.md


=================================
ARCHITECTURE REVIEW
=================================
Using ARCHITECTURE_REVIEW.md, review the solution architecture across app, flows, and lists. Write outputs to ./reports/2026-07-15/ and summarize the top findings in chat.

INPUTS:
* Power App exported JSON
* Power Automate exported JSON
- Requirements.md
- Readme.md
- Architecture.md


=================================
CONSISTENCY REVIEW
=================================
Using CONSISTENCY_REVIEW.md, review app, flows, and lists for drift, duplication, and inconsistencies across the solution. Write outputs to ./reports/2026-07-15/

INPUTS:
* Power App export
* Flow export
- Requirements
- Architecture.md
- Configuration documentation
- SharePoint schema
- Dataverse schema
- Prompt definitions


=================================
DATA CONTRACT REVIEW
=================================
Using DATA_CONTRACT_REVIEW.md, review the data contracts between app, flows, and lists (Power App ↔ Flow ↔ SharePoint). Write outputs to ./reports/2026-07-15/

INPUTS:
* Power App export
* Power Automate export
Requirements
SharePoint schema
Dataverse schema
API documentation
Prompt definitions
Configuration documentation


=================================
POWER AUTOMATE REVIEW
=================================
Using POWER_AUTOMATE_REVIEW.md, review the flow definitions under flows. Write outputs to ./reports/2026-07-15/

INPUTS:
* flow.json
requirements.md
architecture.md
related app export


=================================
POWER APP REVIEW
=================================
Using POWER_APP_REVIEW.md, review the canvas app under app. Write outputs to ./reports/2026-07-15/

INPUTS:
Power App export JSON
Requirements.md
Architecture.md
Related flow exports


=================================
PowerFX REVIEW
=================================
Using POWERFX_REVIEW.md, review the PowerFx formulas extracted from the canvas app under app. Write outputs to ./reports/2026-07-15/

INPUTS:
app.json
flow.json


=================================
DOMAIN-SPECIFIC REVIEW RULES
=================================
For insurance, enrollment, census, coverage, and presentation-generation workflows, pay special attention to:

- Coverage lists that differ across screens, flows, prompts, mappings, templates, or SharePoint configuration.
- Product names that are spelled differently in different places.
- Prompt outputs that use different field names than downstream parsing expects.
- Power Apps dropdown values that do not match flow switch cases.
- Flow switch cases that do not match AI Builder prompt names.
- Placeholder names in templates that do not match replacement logic.
- SharePoint rule values that do not match normalized field names.
- Required fields that are enforced in one place but not another.
- Validation rules that exist in documentation but not in implementation.
- Implementation logic that exists but is not documented in the requirements.




=================================
CREATE .VENV
=================================
cd path\to\codereview\folder
python -m venv .venv
.venv\Scripts\activate

=================================
REMOVE .VENV
=================================
deactivate
Remove-Item -Recurse -Force .venv


=================================
CONVERT MD TO PDF
=================================
# INSTALL REQUIREMENTS
# Create .venv first
pip install pywin32 markdown


# MD_TO_PDF USAGE
cd path\to\scripts
python md_to_pdf.py .\reports\FULL\PATH\TO\REPORT.md

** make sure there are two spaces after each of the Solution lines to indicate a new line / line break, otherwise it will all be concatenated into one long paragraph.


