#!/usr/bin/env sh

now=`date "+%p %R %A"`
FvwmCommand "SendToModule TaskBarAmy ChangeButton timer title \"$now\" "
