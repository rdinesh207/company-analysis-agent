import type { MemoCard as MemoCardType } from "../types";

const CARDS: MemoCardType[] = [
  { id: "investment", label: "Investment recommendation" },
  { id: "company", label: "Company overview" },
  { id: "market", label: "Market analysis" },
  { id: "competitors", label: "Competitor analysis" },
  { id: "risk", label: "Risk analysis" },
  { id: "founder-questions", label: "3 sharpest founder questions" },
];

interface MemoGridProps {
  onSelect: (sectionId: MemoCardType["id"]) => void;
}

export default function MemoGrid({ onSelect }: MemoGridProps) {
  return (
    <div className="memo-grid" role="navigation" aria-label="Memo sections">
      {CARDS.map((card) => (
        <button
          key={card.id}
          type="button"
          className="memo-card"
          onClick={() => onSelect(card.id)}
        >
          {card.label}
        </button>
      ))}
    </div>
  );
}
