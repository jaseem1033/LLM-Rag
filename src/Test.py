from RagPipeline import RagPipeline

rag = RagPipeline()

# # Ingest documents
# rag.ingest_document("""
# Our refund policy: We offer a 14-day money-back guarantee for all annual plans.
# Monthly plans can be cancelled anytime but are not refundable.
# To request a refund, email support@example.com with your order ID.
# """, source="refund-policy.md")

# rag.ingest_document("""
# Pricing Plans:
# - Starter: $9/month or $90/year (save $18)
# - Pro: $29/month or $290/year (save $58)
# - Enterprise: Custom pricing, contact sales
# All plans include 14-day free trial.
# """, source="pricing.md")

# Query
answer = rag.query("how are you")
print(answer)