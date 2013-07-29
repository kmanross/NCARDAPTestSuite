
; Don't forget to replace USERNAME & PASSWORD withyour credentials
; Also, don't forget to replace @ with %40 in USERNAME
; Eg. manross@ucar.edu should be manross%40ucar.edu

  url      = "http://USERNAME:PASSWORD@castle.ucar.edu/thredds/dodsC/ds083.2"
  filename = url + "best"
 
  exists = isfilepresent(filename)
  if(.not.exists) then 
    print("OPeNDAP isfilepresent test unsuccessful.")
    print("Either file doesn't exist, or NCL does not have OPeNDAP capabilities on this system")
  else
    print("OPeNDAP isfilepresent test successful.")
    f = addfile(filename,"r")
    vars = getfilevarnames(f)
    print(vars)   ; should be (in any order): "l","j","i","cross","aloan",
                  ; "shot","order","bears"
  end if
