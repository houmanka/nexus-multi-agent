from dataclasses import dataclass

import nexusrpc


@dataclass
class QualificationInput:
    """
    Input for QualificationService.
    LTV ratio = loan_amount / property_value. High LTV (> 80%) indicates higher risk.

    Attributes:
        application_id: Unique loan application identifier — used as the workflow ID for deduplication
        loan_amount: Amount the applicant wants to borrow, in AUD
        property_value: Appraised market value of the property, in AUD
    """
    application_id: str
    loan_amount: float
    property_value: float

@dataclass
class QualificationResult:
    """
    Attributes:
        is_qualified: Whether the applicant passes the basic qualification check
        reason: Human-readable explanation of the qualification decision
    """
    is_qualified: bool
    reason: str


@nexusrpc.service
class QualificationService:
    qualify: nexusrpc.Operation[QualificationInput, QualificationResult]


@dataclass
class IncomeInput:
    """
    Attributes:
        application_id: Unique loan application identifier — used as the workflow ID for deduplication
        stated_income: Annual income as declared by the applicant, in AUD
        employment_type: Nature of employment — full-time, casual, or self-employed
        payslip_text: Raw payslip text for LLM extraction — never leaves the income team's infrastructure
    """
    application_id: str
    stated_income: float
    employment_type: str
    payslip_text: str


@dataclass
class IncomeVerificationResult:
    """
    Attributes:
        verified_income: LLM-verified annual income extracted from the payslip, in AUD
        employer: Employer name extracted from the payslip
        employment_type: Confirmed employment type after verification
        is_verified: Whether the stated income could be confirmed against the payslip
    """
    verified_income: float
    employer: str
    employment_type: str
    is_verified: bool

@nexusrpc.service
class IncomeVerificationService:
    verify: nexusrpc.Operation[IncomeInput, IncomeVerificationResult]


@dataclass
class ServiceabilityInput:
    """
    Attributes:
        application_id: Unique loan application identifier — used as the workflow ID for deduplication
        verified_income: LLM-verified annual income from IncomeVerificationResult, in AUD
        loan_amount: Amount the applicant wants to borrow, in AUD
        property_value: Appraised market value of the property, in AUD
    """
    application_id: str
    verified_income: float
    loan_amount: float
    property_value: float

@dataclass
class ServiceabilityResult:
    """
    Attributes:
        can_service: Whether the applicant can meet repayments at the regulatory buffer rate
        explanation: Claude-generated plain-English explanation of the serviceability decision
        monthly_repayment: Estimated monthly repayment amount, in AUD
    """
    can_service: bool
    explanation: str
    monthly_repayment: float

@nexusrpc.service
class ServiceabilityService:
    assess: nexusrpc.Operation[ServiceabilityInput, ServiceabilityResult]