
# AICS-201
# AI ETHICS, GOVERNANCE AND LEGAL COMPLIANCE ASSESSMENT

## Organisation: SecureFinance Africa

## 1. Executive Summary

This assessment evaluates the legal and regulatory risks associated
with a fictional AI-powered financial assessment system.

The assessment focuses on the Nigeria Data Protection Act 2023,
the European Union Artificial Intelligence Act, and international
ethical frameworks established by UNESCO and the OECD.

The practical investigation identified disparities in simulated
financial approval decisions based on gender and geographical region.

The findings indicate that the fictional system requires significant
fairness, transparency, privacy and accountability safeguards
before any real-world deployment could be considered.

## 2. Nigeria Data Protection Act 2023

The Nigeria Data Protection Act 2023 establishes the legal framework
for processing personal data in Nigeria.

The Act is relevant to SecureFinance Africa because the organisation
would process customer information for financial assessment.

### 2.1 Section 24 – Principles of Personal Data Processing

Requirement:
Personal data must be processed fairly, lawfully and transparently.
Data collection must be limited to specified and legitimate purposes.

Assessment:
The simulated system collects financial and demographic attributes.
Gender and geographical location are included in the fairness audit.

Risk:
Using demographic characteristics to influence financial approval
decisions may create discriminatory outcomes and undermine fairness.

Recommended controls:
- Apply data minimisation.
- Document processing purposes.
- Review the necessity of each model feature.
- Maintain accurate and secure records.

### 2.2 Section 25 – Lawful Basis of Processing

Requirement:
Personal data processing must have an applicable lawful basis.

Assessment:
SecureFinance Africa must identify and document the appropriate
lawful basis for every relevant processing activity.

Recommended controls:
- Maintain a record of processing activities.
- Document the selected lawful basis.
- Do not assume consent is always necessary or appropriate.
- Review legitimate interests against data subject rights.

### 2.3 Section 27 – Information to Data Subjects

Requirement:
Data subjects must receive information about processing,
including the existence and consequences of automated
decision-making and profiling.

Assessment:
Applicants should understand when automated systems influence
their financial applications.

Recommended controls:
- Publish an accessible privacy notice.
- Explain the purpose of automated assessments.
- Disclose relevant consequences of profiling.
- Explain how applicants can challenge decisions.

### 2.4 Section 28 – Data Privacy Impact Assessment

Requirement:
A Data Privacy Impact Assessment (DPIA) must be conducted
before processing where the processing is likely to create
high risks to individuals' rights and freedoms.

Assessment:
Financial profiling and automated lending decisions can have
significant consequences for affected individuals.

A DPIA should therefore be completed before deployment.

The assessment should examine:
- Processing activities and purposes.
- Necessity and proportionality.
- Risks to data subjects.
- Proposed safeguards and mitigation measures.

Where high risks remain despite proposed safeguards,
the Commission must be consulted before processing.

### 2.5 Section 29 – Data Processor Obligations

Requirement:
Data processors must comply with applicable data protection
obligations and implement appropriate technical and organisational
safeguards.

Recommended controls:
- Establish written processor agreements.
- Assess third-party service providers.
- Monitor outsourced data processing.
- Require appropriate security measures.

### 2.6 Section 32 – Data Protection Officer

Requirement:
A data controller of major importance must designate a
qualified Data Protection Officer.

Recommended controls:
- Assign a competent DPO.
- Establish reporting and escalation responsibilities.
- Monitor compliance with privacy policies.
- Maintain contact with the NDPC.

### 2.7 Section 37 – Automated Decision-Making

Requirement:
Individuals have a right not to be subject to decisions based
solely on automated processing, including profiling, where
those decisions produce legal or similar significant effects,
subject to the statutory exceptions.

Where an exception applies, suitable safeguards must include
human intervention, the opportunity to express a point of view,
and the ability to contest the decision.

Assessment:
An automated financial approval or rejection may significantly
affect an applicant.

Recommended controls:
- Provide meaningful human review.
- Allow applicants to challenge decisions.
- Record human interventions and overrides.
- Provide understandable decision explanations.

### 2.8 Section 39 – Data Security

Requirement:
Appropriate technical and organisational measures must protect
the security, integrity and confidentiality of personal data.

Recommended controls:
- Encrypt sensitive information.
- Implement role-based access control.
- Maintain security logs.
- Perform periodic security testing.
- Establish backup and recovery procedures.

### 2.9 Section 40 – Personal Data Breaches

Requirement:
A controller must notify the NDPC within 72 hours of becoming
aware of a breach likely to create a risk to individuals' rights
and freedoms. High-risk breaches also require communication
to affected individuals as provided by the Act.

Recommended controls:
- Establish an incident response plan.
- Maintain a breach register.
- Define notification responsibilities.
- Preserve investigation evidence.

## 3. EU Artificial Intelligence Act

The EU AI Act is Regulation (EU) 2024/1689.

### 3.1 Scope and Applicability

The organisation must assess whether its activities fall within
the territorial scope of Article 2.

The Act can apply to providers and deployers outside the EU
where the output produced by an AI system is used in the Union.

### 3.2 Creditworthiness Classification

Annex III, point 5(b), identifies AI systems intended to evaluate
the creditworthiness of natural persons or establish their credit
score as high-risk.

AI systems used specifically for financial fraud detection are
excluded from this particular Annex III category.

The classification must be assessed against the actual intended
purpose and use of the system.

### 3.3 High-Risk AI Safeguards

Relevant requirements include:

- Risk management.
- Data governance.
- Technical documentation.
- Record keeping.
- Transparency and information to deployers.
- Human oversight.
- Accuracy, robustness and cybersecurity.
- Post-market monitoring.

### 3.4 Fundamental Rights Impact Assessment

Article 27 requires specified deployers, including deployers of
systems under Annex III points 5(b) and 5(c), to conduct a
fundamental rights impact assessment before deployment,
subject to the Article's detailed conditions and exceptions.

### 3.5 Implementation Timetable

The assessment must reflect the applicable amendments to the
AI Act, including Regulation (EU) 2026/1744.

As at 11 November 2026, the application of the relevant Annex III
high-risk requirements has been deferred to 2 December 2027.

The organisation should monitor further official amendments
and implementation guidance.

## 4. UNESCO AI Ethics Recommendation

UNESCO's 2021 Recommendation on the Ethics of Artificial
Intelligence provides international guidance on responsible AI.

Relevant principles include:

- Protection of human rights and human dignity.
- Fairness and non-discrimination.
- Transparency and explainability.
- Human oversight.
- Responsibility and accountability.
- Privacy and data protection.

Application:
SecureFinance Africa should ensure that automated decisions
do not undermine individual rights or exclude applicants
through unjustified discriminatory practices.

## 5. OECD AI Principles

The OECD AI Principles were updated in 2024.

The relevant principles include:

1. Inclusive growth and sustainable development.
2. Respect for human rights and democratic values.
3. Transparency and explainability.
4. Robustness, security and safety.
5. Accountability.

Application:
The organisation should maintain traceable AI decisions,
provide meaningful explanations and adopt continuous risk
management throughout the AI system lifecycle.

## 6. Compliance Gaps Identified

The following are preliminary gaps identified from the
fictional system design and practical simulation.

| Area | Identified gap | Recommended action |
|---|---|---|
| Fairness | Group approval disparities | Bias mitigation and recurring audits |
| Transparency | Automated decisions require explanations | Applicant notification and explanations |
| Privacy | DPIA not yet documented | Complete a DPIA before deployment |
| Human oversight | Review process not yet implemented | Establish meaningful human review |
| Accountability | Operational responsibilities need formal approval | Establish governance oversight |
| Security | Production controls not tested | Conduct security assessment |
| Data governance | Lawful basis not documented | Maintain processing records |

These are preliminary assessment findings, not a declaration
that an actual organisation has violated the law.

## 7. Overall Compliance Recommendations

SecureFinance Africa should:

1. Complete a formal Data Privacy Impact Assessment.
2. Document lawful processing bases.
3. Remove unjustified demographic decision penalties.
4. Establish meaningful human review.
5. Provide applicant notification and appeal mechanisms.
6. Implement data security and retention controls.
7. Document processor relationships.
8. Conduct regular fairness and model validation audits.
9. Maintain an AI incident response procedure.
10. Monitor relevant legal and regulatory developments.

## 8. Conclusion

The assessment demonstrates that responsible AI deployment
requires more than technical model performance.

Legal compliance, fairness, transparency, privacy and
organisational accountability must be integrated throughout
the AI lifecycle.

The simulated SecureFinance Africa system demonstrates
measurable disparities that require remediation before
any production deployment could be considered.

This assessment is educational and does not constitute
a formal legal opinion or certification of compliance.

## 9. References

1. Federal Republic of Nigeria. (2023). Nigeria Data Protection Act 2023.
   https://placng.org/i/wp-content/uploads/2023/06/Nigeria-Data-Protection-Act-2023.pdf

2. European Parliament and Council. (2024).
   Regulation (EU) 2024/1689 – Artificial Intelligence Act.
   https://eur-lex.europa.eu/eli/reg/2024/1689/oj

3. European Parliament and Council. (2026).
   Regulation (EU) 2026/1744.
   https://eur-lex.europa.eu/eli/reg/2026/1744/oj

4. UNESCO. (2021).
   Recommendation on the Ethics of Artificial Intelligence.
   https://www.unesco.org/en/articles/recommendation-ethics-artificial-intelligence

5. OECD. (2024).
   OECD AI Principles.
   https://oecd.ai/en/ai-principles
