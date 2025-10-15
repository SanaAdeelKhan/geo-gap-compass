"use client";
// FILE: app/dashboard/domains/page.jsx
// =============================================================================

import DomainInsights from "@/components/DomainInsights";

export default function DomainsPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <DomainInsights />
    </div>
  );
}