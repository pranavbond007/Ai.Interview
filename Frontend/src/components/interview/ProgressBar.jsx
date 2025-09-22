export default function ProgressBar({ current, total }) {
  const percentage = (current / total) * 100

  return (
    <div className="w-32">
      <div className="flex justify-between text-xs text-neutral-400 mb-1">
        <span>Progress</span>
        <span>{current}/{total}</span>
      </div>
      <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
        <div 
          className="h-full bg-neon-blue transition-all duration-300"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  )
}
