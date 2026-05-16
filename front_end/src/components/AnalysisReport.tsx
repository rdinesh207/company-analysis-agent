import type { CompanyAnalysisResponse } from "../types";
import InvestmentSection from "./InvestmentSection";
import ExpandableDetailSections from "./ExpandableDetailSections";

interface AnalysisReportProps {
  data: CompanyAnalysisResponse;
}

export default function AnalysisReport({ data }: AnalysisReportProps) {
  return (
    <article className="report">
      <InvestmentSection data={data} />
      <ExpandableDetailSections data={data} />
    </article>
  );
}
