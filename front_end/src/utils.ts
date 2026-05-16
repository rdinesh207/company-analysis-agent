import type { CompetitorPosition, Verdict } from "./types";

export function verdictTone(verdict: Verdict): "positive" | "neutral" | "negative" {
  const v = verdict.toLowerCase();
  if (v.includes("bull")) return "positive";
  if (v.includes("bear") || v.includes("risk") || v === "pass") return "negative";
  return "neutral";
}

export function positionLabel(position: CompetitorPosition): string {
  const p = position.toLowerCase();
  if (p === "stronger") return "Stronger";
  if (p === "weaker") return "Weaker";
  return "Comparable";
}

export function positionTone(
  position: CompetitorPosition,
): "stronger" | "comparable" | "weaker" {
  const p = position.toLowerCase();
  if (p === "stronger") return "stronger";
  if (p === "weaker") return "weaker";
  return "comparable";
}

export function scrollToSection(id: string) {
  document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
}

export function normalizeWebsite(raw: string): string {
  const trimmed = raw.trim();
  if (!trimmed) return "";
  if (/^https?:\/\//i.test(trimmed)) return trimmed;
  if (!trimmed.includes(".")) return "";
  return `https://${trimmed}`;
}
