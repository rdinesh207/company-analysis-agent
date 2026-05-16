import { useState } from "react";
import type { CompanyAnalysisResponse, DetailSectionId } from "../types";
import CompanyOverviewSection from "./CompanyOverviewSection";
import MarketSection from "./MarketSection";
import CompetitorSection from "./CompetitorSection";
import RiskSection from "./RiskSection";

const SECTIONS: { id: DetailSectionId; label: string }[] = [
  { id: "company", label: "Company overview" },
  { id: "market", label: "Market analysis" },
  { id: "competitors", label: "Competitor analysis" },
  { id: "risk", label: "Risk analysis" },
];

interface ExpandableDetailSectionsProps {
  data: CompanyAnalysisResponse;
}

export default function ExpandableDetailSections({
  data,
}: ExpandableDetailSectionsProps) {
  const [expanded, setExpanded] = useState<Set<DetailSectionId>>(new Set());

  function toggle(id: DetailSectionId) {
    setExpanded((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  function renderContent(id: DetailSectionId) {
    switch (id) {
      case "company":
        return <CompanyOverviewSection data={data} embedded />;
      case "market":
        return <MarketSection data={data} embedded />;
      case "competitors":
        return <CompetitorSection data={data} embedded />;
      case "risk":
        return <RiskSection data={data} embedded />;
    }
  }

  return (
    <div className="accordion-list">
      {SECTIONS.map((section) => {
        const isOpen = expanded.has(section.id);
        return (
          <div
            key={section.id}
            className={`accordion-item${isOpen ? " accordion-item-open" : ""}`}
          >
            <button
              type="button"
              className="accordion-header"
              aria-expanded={isOpen}
              onClick={() => toggle(section.id)}
            >
              <span className="accordion-label">{section.label}</span>
              <span className="accordion-icon" aria-hidden="true">
                {isOpen ? "−" : "+"}
              </span>
            </button>
            {isOpen ? (
              <div className="accordion-body">{renderContent(section.id)}</div>
            ) : null}
          </div>
        );
      })}
    </div>
  );
}
