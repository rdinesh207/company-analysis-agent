import type { CompanyAnalysisResponse } from "../types";

interface RiskSectionProps {
  data: CompanyAnalysisResponse;
}

const RISK_ROWS: {
  key: keyof CompanyAnalysisResponse["risk_analysis"];
  label: string;
}[] = [
  { key: "market_risk", label: "Market" },
  { key: "competition_risk", label: "Compete" },
  { key: "execution_risk", label: "Execution" },
  { key: "monetization_risk", label: "Monetization" },
];

export default function RiskSection({ data }: RiskSectionProps) {
  const risks = data.risk_analysis;

  return (
    <section id="risk" className="detail-card">
      <h3 className="detail-card-title">Risk analysis</h3>
      <ul className="risk-list">
        {RISK_ROWS.map(({ key, label }) => (
          <li key={key} className="risk-row">
            <span className="risk-category">{label}</span>
            <span className="pill pill-medium">Medium</span>
            <p className="risk-text">{risks[key]}</p>
          </li>
        ))}
      </ul>
    </section>
  );
}
