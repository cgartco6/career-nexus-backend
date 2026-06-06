from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import json

# App Module Domain Inclusions
from config.security import SecurityEngine
from services.ai_service import AIService
from services.payment_service import PaymentGatewayHub
from services.payout_service import AutomatedPayoutLedger
from services.document_service import DocumentCreatorService
from middleware.compliance import RegulatoryComplianceMiddleware

app = FastAPI(
    title="CareerNexus Core Platform API Engine",
    version="2.0.0",
    docs_url="/api/v1/secure-blueprint-docs"
)

# Apply global security configuration architectures
app.add_middleware(RegulatoryComplianceMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Tighten down to explicit mobile apps / web app production domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core Mock In-Memory DB state structures for Cart Infrastructure
USER_CARTS: Dict[str, List[dict]] = {}

# Initialize Core Services
ai_engine = AIService()
payment_hub = PaymentGatewayHub()

# --- SECURITY / ECOMMERCE SHOPPING CART ROUTING ---

@app.post("/api/v1/cart/add", tags=["E-Commerce Engine"])
async def add_item_to_cart(user_id: str, item_id: str, price_zar: float, description: str):
    if user_id not in USER_CARTS:
        USER_CARTS[user_id] = []
    cart_item = {"item_id": item_id, "price_zar": price_zar, "description": description}
    USER_CARTS[user_id].append(cart_item)
    return {"status": "Success", "message": "Item registered into system cart sync", "current_cart": USER_CARTS[user_id]}

@app.post("/api/v1/cart/checkout", tags=["E-Commerce Engine"])
async def process_cart_checkout(user_id: str, gateway_choice: str, return_url: str):
    if user_id not in USER_CARTS or not USER_CARTS[user_id]:
        raise HTTPException(status_code=400, detail="User target profile shopping cart is entirely empty")
        
    total_price = sum(item["price_zar"] for item in USER_CARTS[user_id])
    tx_ref = f"TXN-{user_id[:4].upper()}-{int(total_price)}"
    
    # Empty cart on checking out routing
    USER_CARTS[user_id] = []
    
    # Process multi-gateway choice handling
    if gateway_choice.lower() == "ozow":
        return payment_hub.initiate_ozow_instant_eft(total_price, tx_ref, return_url, return_url)
    elif gateway_choice.lower() == "payfast":
        return payment_hub.generate_payfast_form_payload(total_price, "CareerNexus Premium Bundle Checkout", return_url)
    elif gateway_choice.lower() == "stripe":
        # Convert ZAR balance estimation down to USD globally
        usd_conversion = total_price / 18.50 
        return payment_hub.initiate_stripe_checkout(usd_conversion, return_url, return_url)
    else:
        # Fallback Direct Ledger entry processing reference
        return {"status": "Pending", "payment_instructions": "Direct Electronic Funds Transfer (EFT) to FNB Core Suite Account Account: 62234567890 Branch: 250655 Reference: " + tx_ref}

# --- WEB & MOBILE FUNCTIONAL AI LOGIC ENDPOINTS ---

@app.post("/api/v1/engine/rewrite-cv", tags=["AI Core Processors"])
async def process_cv_rewrite(target_industry: str = Form(...), file: UploadFile = File(...)):
    raw_bytes = await file.read()
    # Decode string safely
    raw_text = raw_bytes.decode("utf-8", errors="ignore")
    
    # Process through core AI pipeline
    optimized_markdown = ai_engine.rewrite_cv_ats_compliant(raw_text, target_industry)
    
    # Create production standard PDF stream format output directly 
    pdf_binary = DocumentCreatorService.generate_pdf_document("ATS OPTIMIZED CV", optimized_markdown)
    
    # Create companion generic template covering document asset concurrently
    cover_letter_raw = ai_engine.generate_cover_letter(optimized_markdown, f"General Management Position in {target_industry}")
    cover_letter_pdf = DocumentCreatorService.generate_pdf_document("TAILORED COVER LETTER", cover_letter_raw)
    
    # Wrap structures tightly inside dynamic programmatic ZIP distribution bundle
    zip_payload = DocumentCreatorService.compress_artifacts_to_zip({
        "ATS_Compliant_CV.pdf": pdf_binary,
        "Professional_Cover_Letter.pdf": cover_letter_pdf
    })
    
    # For execution verification output details
    return {
        "status": "Success",
        "industry_aligned": target_industry,
        "markdown_preview": optimized_markdown[:500] + "...",
        "zip_bundle_size_bytes": len(zip_payload)
    }

@app.post("/api/v1/engine/ai-tutor", tags=["AI Core Processors"])
async def interact_with_ai_tutor(cv_context: str = Form(...), user_answer: str = Form(...), interview_stage: str = Form(...)):
    tutor_json_response = ai_engine.run_ai_tutor_session(cv_context, user_answer, interview_stage)
    return {"status": "Success", "evaluation": json.loads(tutor_json_response)}

# --- PROGRAMMATIC SPLIT REAL-TIME PAYOUT SIMULATOR ---

@app.post("/api/v1/payouts/process-reconciliation", tags=["Automated Finance Ledger Tracking"])
async def process_transaction_reconciliation(transaction_id: str, captured_net_zar_amount: float):
    """
    Triggers checking systems to verify automated platform financial distributions.
    Separates payouts precisely into 50%, 10%, and 40% allocations.
    """
    payout_ledger_entry = AutomatedPayoutLedger.split_settlement_funds(transaction_id, captured_net_zar_amount)
    return {
        "ledger_status": "Calculated-And-Cleared",
        "distribution_metrics": payout_ledger_entry
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
