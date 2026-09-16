from pydantic import BaseModel, ValidationError

class M(BaseModel):
    a: str                  # ?
    b: str = "x"            # ?
    c: str | None = None    # ?
    d: str | None           # ?

try:
    m = M(a="1")
    print("成功:", m)
except ValidationError as e:
    print("失败:")
    for line in str(e).splitlines()[1:]:
        if line.strip():
            print("   ", line.strip())