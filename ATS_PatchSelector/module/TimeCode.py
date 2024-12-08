def calcClockDisplay(totalFrame):
    framerate = project.cookRate

    frame = int(totalFrame % framerate)
    second = int(totalFrame // framerate % 60)
    minute = int(totalFrame // (framerate * 60) % 60)
    hour = int(totalFrame // (framerate * 3600) % 60)

    frameZero = str(frame).zfill(2)
    secondZero = str(second).zfill(2)
    minuteZero = str(minute).zfill(2)
    hourZero = str(hour).zfill(2)

    time = hourZero + ':' + minuteZero + ':' + secondZero + ':' + frameZero

    return time 

def calcFrame(totalFrame):
    framerate = project.cookRate
    frame = int(totalFrame % framerate)

    return frame

def calcSecond(totalFrame):
    framerate = project.cookRate
    second = int(totalFrame // framerate % 60)

    return second

def calcMinute(totalFrame):
    framerate = project.cookRate
    minute = int(totalFrame // (framerate * 60) % 60)

    return minute

def calcHour(totalFrame):
    framerate = project.cookRate
    hour = int(totalFrame // (framerate * 3600) % 60)

    return hour

def calcTotalFrame(timeDisplay: str):
    framerate = project.cookRate
    if len(timeDisplay) == 11:
        hour = int(timeDisplay[0:2])
        minute = int(timeDisplay[3:5])
        second = int(timeDisplay[6:8])
        frame = int(timeDisplay[9:])
        totalFrame = frame + (second * framerate) + (minute * framerate * 60) + (hour * framerate * 3600)
    else:
        totalFrame = ""
    return totalFrame

def getHourByClock(timeDisplay: str):
    if len(timeDisplay) == 11:
        hour = int(timeDisplay[0:2])
    else:
        return
    return hour

def getMinuteByClock(timeDisplay: str):
    if len(timeDisplay) == 11:
        minute = int(timeDisplay[3:5])
    else:
        return
    return minute

def getSecondByClock(timeDisplay: str):
    if len(timeDisplay) == 11:
        second = int(timeDisplay[6:8])
    else:
        return
    return second

def getFrameByClock(timeDisplay: str):
    if len(timeDisplay) == 11:
        frame = int(timeDisplay[9:])
    else:
        return
    return frame