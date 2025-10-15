"use client";
// =============================================================================
// FILE: components/Navigation.jsx (Enhanced with Active State)
// =============================================================================

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, TrendingUp, Users, Globe, BarChart3 } from "lucide-react";

export default function Navigation() {
  const pathname = usePathname();

  const navItems = [
    { label: "Dashboard", href: "/dashboard", icon: Home },
    { label: "Heatmap", href: "/dashboard/heatmap", icon: TrendingUp },
    { label: "Competitors", href: "/dashboard/competitors", icon: Users },
    { label: "Domains", href: "/dashboard/domains", icon: Globe },
    { label: "Prompts", href: "/dashboard/prompts", icon: BarChart3 },
  ];

  const isActive = (href) => {
    if (href === "/dashboard") {
      return pathname === href;
    }
    return pathname.startsWith(href);
  };

  return (
    <nav className="bg-white border-b shadow-sm">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex items-center justify-between">
          <div className="flex gap-6">
            {navItems.map((item) => {
              const active = isActive(item.href);
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center gap-2 py-4 border-b-2 transition ${
                    active
                      ? "border-blue-600 text-blue-600"
                      : "border-transparent text-gray-700 hover:text-blue-600 hover:border-blue-300"
                  }`}
                >
                  <item.icon size={18} />
                  <span className="font-medium">{item.label}</span>
                </Link>
              );
            })}
          </div>
          
          {/* Logo/Title */}
          <div className="hidden md:block">
            <Link href="/" className="text-xl font-bold text-gray-900">
              GEO Gap Compass
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}