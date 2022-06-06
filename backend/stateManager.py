from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class StateManager:
    driver = None
    def setDriver(self, driver):
        self.driver = driver
        return self
    def wasTwoWeeksAgo(self, date: str):
        d1 = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
        d2 = datetime.now()
        return d2 - d1 > timedelta(weeks=2)
    def currentlyHasCovid(self, uuid):
        if not self.driver.hasCovid(uuid): return False
        date = self.driver.dateReported(uuid)
        if self.wasTwoWeeksAgo(date): 
            self.driver.flagWithCovid(uuid, False)
            return False
        return True
    