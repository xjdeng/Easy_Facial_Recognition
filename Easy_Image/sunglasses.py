try:
    from . import detect
except ImportError:
    import detect

import math
    
eye_detector = detect.DetectorParams('cascade','haar','haarcascade_eye.xml')

def _to_deg(rad):
    return rad*180/math.pi

def run(person, sunglass, enlarge = 1.1, target = None):
    faces = person.detect_faces()
    eyes = None
    face = None
    for f in faces:
        found_eyes = f.detect_faces_simple(eye_detector)
        if len(found_eyes) == 2:
            eyes = found_eyes
            face = f
            break
    if eyes is None:
        return None
    if eyes[0].face.left() < eyes[1].face.left():
        eye1 = eyes[0]
        eye2 = eyes[1]
    else:
        eye1 = eyes[1]
        eye2 = eyes[0]
    ef1 = eye1.face
    ef2 = eye2.face
    angle1 = math.atan((ef2.top() - ef1.top())/(ef2.left() - ef1.left()))
    angle2 = math.atan((ef2.bottom() - ef2.bottom())/(ef2.right() - ef1.right()))
    angle = _to_deg((angle1 + angle2)/2)
    ff = face.face
    sunglass.resize(round(enlarge*(ff.right() - ff.left())), \
                    round(enlarge*(ef2.bottom() - ef1.top())))
    sunglasses2 = sunglass.rotate(angle)
    sy, sx, _ = sunglasses2.getimg().shape
    if target is None:
        x = round(ff.left() - sx*(enlarge - 1)/2)
        y = round(ef1.top() + ff.top() - sy*(enlarge - 1)/2)
        #target = (ff.left(), ef1.top() + ff.top())
        target = (max(0,x),max(0,y))
    try:
        return person.paste(sunglasses2, target[0], target[1])
    except detect.InvalidOperation:
        return None