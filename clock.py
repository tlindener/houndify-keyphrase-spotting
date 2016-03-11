class alarmclock:
    def  __init__(self, allResults):
        for result in allResults:
            if result.has_key("AlarmCommandKind"):
                if result["AlarmCommandKind"] == "AlarmSetCommand":
                    self.setMultiple(result["NativeData"])

    def setMultiple(self, nativeData):
        if not nativeData.has_key("Alarms"):
            print 'Could not find any alarms'
            return
        for alarmData in nativeData["Alarms"]:
            self.setSingle(alarmData)

    def setSingle(self, alarmData):
        """
        given data in the form
        {
          "Hour":9,
          "Title":"wake up",
          "DaysOfWeek":[

          ],
          "IsWake":True,
          "InvalidDates":[

          ],
          "Second":0,
          "Minute":0
        }
        """
        hour = alarmData["Hour"]
        minute = alarmData["Minute"]
        second = alarmData["Second"]
        if alarmData.has_key("Title"):
            title = alarmData["Title"]
        else:
            title = ''

        print "If I could I would set an alarm for "+str(hour)+":"+str(minute)+":"+str(second)+" and call it "+title+"."
