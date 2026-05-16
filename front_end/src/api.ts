import type { AnalyzeRequest, CompanyAnalysisResponse } from "./types";

const API_BASE =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") ?? "/api";

export async function analyzeCompany(
  payload: AnalyzeRequest,
): Promise<CompanyAnalysisResponse> {
  const response = await fetch(`${API_BASE}/v1/investment-analysis`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const detail = await response.text().catch(() => "");
    throw new Error(
      detail || `Analysis failed (${response.status} ${response.statusText})`,
    );
  }

  return response.json() as Promise<CompanyAnalysisResponse>;
}
