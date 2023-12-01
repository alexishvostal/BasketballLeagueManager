import React, { useState } from 'react';
import TeamDropdown from '../components/TeamDropdown';
import WinLossRecord from '../components/WinLossRecord';

export default function Report() {
  const [selectedTeam, setSelectedTeam] = useState(1);

  return (
    <div>
      <TeamDropdown selectedTeam={selectedTeam} setSelectedTeam={setSelectedTeam} />
      <div>Your team is: {selectedTeam}</div>
      <WinLossRecord selectedTeam={selectedTeam} />
    </div>
  );
}
