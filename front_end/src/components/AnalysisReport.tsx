import type { CompanyAnalysisResponse } from "../types";
import InvestmentSection from "./InvestmentSection";
import CompanyOverviewSection from "./CompanyOverviewSection";
import MarketSection from "./MarketSection";
import CompetitorSection from "./CompetitorSection";
import RiskSection from "./RiskSection";
import FounderQuestionsSection from "./FounderQuestionsSection";

interface AnalysisReportProps {
  data: CompanyAnalysisResponse;
}

export default function AnalysisReport({ data }: AnalysisReportProps) {
  const website = data.company_website;

  return (
    <article className="report">
      {website ? (
        <p className="hero-description" style={{ marginBottom: 24 }}>
          Website:{" "}
          <a href={website} target="_blank" rel="noreferrer">
            {website}
          </a>
        </p>
      ) : null}

      <InvestmentSection data={data} />

      <div className="detail-grid" style={{ marginTop: 16 }}>
        <CompanyOverviewSection data={data} />
        <MarketSection data={data} />
        <CompetitorSection data={data} />
        <RiskSection data={data} />
        <FounderQuestionsSection data={data} />
      </div>
    </article>
  );
}
