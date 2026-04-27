QA Testing Project – Grădina Crăciun E-commerce Platform
Application URL: https://gradina-craciun-668739da08cd.herokuapp.com

Overview
This project demonstrates end-to-end manual QA testing of an e-commerce web application.
The goal was to validate core user flows, identify defects, and assess release readiness using industry-standard tools and practices.

Tools & Technologies
- Test Management: TestRail
- Bug Tracking: Jira
- Documentation: Confluence
- Automation (basic): Playwright
- Language: TypeScript

Testing Scope
The following areas were tested:
- Authentication (Login / Logout)
- Product Catalog (search, filters, display)
- Cart functionality (add, update, remove)
- Checkout process (delivery details, validation)
- Order submission & confirmation

Test Execution Summary
- Total test cases: 57
- Passed: 53
- Failed: 2
- Blocked: 2
- Pass rate: 93%

Key Defects Identified
- Critical Bug – Incorrect Shipping Address in Confirmation Email (GC-35)
Shipping address in confirmation email does not match user input
- High risk: may lead to incorrect deliveries
- Impact: affects core business functionality
- Medium Bug – Cart Not Cleared After Order (GC-34)
Cart items remain visible after successful order submission
- Impact: user confusion, potential duplicate actions

QA Analysis & Decision
Although most test cases passed and core flows are functional, a critical data integrity issue was identified.

Final Decision: NO GO
The application is not ready for release due to:

Incorrect shipping address in confirmation email
Risk of failed or incorrect deliveries

QA Workflow Followed
Test Planning → Test Execution → Defect Logging → Retesting → Regression Testing → Release Decision

Project Artifacts
- Test Plan & Execution Summary (Confluence)
- Test Execution Report (TestRail)
- Defect Tracking (Jira)

(Links can be provided upon request)

Author
Anamaria Anghel-Tanase
QA Engineer
