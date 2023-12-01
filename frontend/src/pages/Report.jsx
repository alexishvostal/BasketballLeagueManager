import React, { useState } from 'react';
import TeamDropdown from '../components/TeamDropdown';
import WinLossRecord from '../components/WinLossRecord';
import TeamRoster from '../components/TeamRoster';

export default function Report() {
  const [selectedTeam, setSelectedTeam] = useState(1);

  return (
    <div>
      <h2>Report</h2>
      <TeamDropdown selectedTeam={selectedTeam} setSelectedTeam={setSelectedTeam} />
      <WinLossRecord selectedTeam={selectedTeam} />
      <TeamRoster selectedTeam={selectedTeam} />
    </div>
  );
}
