export default function StatCard({ label, value, hint }) {
  return (
    <div className="card">
      <p className="text-sm text-slate-600">{label}</p>
      <p className="text-2xl font-bold text-leaf mt-2">{value}</p>
      {hint ? <p className="text-xs text-slate-500 mt-1">{hint}</p> : null}
    </div>
  );
}
