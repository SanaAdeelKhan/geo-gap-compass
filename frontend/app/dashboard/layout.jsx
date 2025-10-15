// FILE: app/dashboard/layout.jsx (Dashboard Layout with Navigation)
// =============================================================================
import Navigation from "@/components/Navigation";

export default function DashboardLayout({ children }) {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      {children}
    </div>
  );
}