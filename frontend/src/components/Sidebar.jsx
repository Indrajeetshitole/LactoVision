import { NavLink } from "react-router-dom";
import {
  BarChart3, Bell, Beef, ClipboardPlus, CloudSun, Database,
  FileText, HeartPulse, Home, Milk, Settings, Sparkles, Wheat,
  X
} from "lucide-react";

const items = [
  ["Dashboard", "/", Home],
  ["Farm", "/farm", Beef],
  ["Cows", "/cows", Beef],
  ["Milk Records", "/milk", Milk],
  ["Feed & Nutrition", "/feed", Wheat],
  ["Health Monitoring", "/health", HeartPulse],
  ["Environment", "/environment", CloudSun],
  ["Milk Prediction", "/prediction", Sparkles],
  ["Recommendations", "/recommendations", ClipboardPlus],
  ["Analytics", "/analytics", BarChart3],
  ["Alerts", "/alerts", Bell],
  ["Reports", "/reports", FileText],
  ["Settings", "/settings", Settings],
  ["System Test", "/system-test", Database],
];

export default function Sidebar({ open, onClose }) {
  return (
    <aside className={`fixed inset-y-0 left-0 z-40 w-72 transform border-r border-slate-200 bg-white transition-transform lg:static lg:translate-x-0 ${open ? "translate-x-0" : "-translate-x-full"}`}>
      <div className="flex h-full flex-col">
        <div className="flex items-center justify-between border-b border-slate-100 px-6 py-5">
          <div>
            <div className="text-2xl font-black tracking-tight text-emerald-700">LactoVision</div>
            <div className="text-xs text-slate-500">Milk Yield Optimization AI</div>
          </div>
          <button onClick={onClose} className="lg:hidden">
            <X size={20} />
          </button>
        </div>

        <nav className="flex-1 overflow-y-auto p-3">
          {items.map(([label, path, Icon]) => (
            <NavLink
              key={path}
              to={path}
              onClick={onClose}
              end={path === "/"}
              className={({ isActive }) =>
                `mb-1 flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition ${
                  isActive
                    ? "bg-emerald-50 text-emerald-700"
                    : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                }`
              }
            >
              <Icon size={18} />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="border-t border-slate-100 p-4 text-xs text-slate-400">
          Phase 1 Foundation
        </div>
      </div>
    </aside>
  );
}
