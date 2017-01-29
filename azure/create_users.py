#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string
import random
import subprocess
import json
import pandas as pd

student_cnt = 81


def generate_pass():
    numbers = [random.choice(string.digits) for _ in range(2)]
    big_letters = [random.choice(string.letters.upper()) for _ in range(7)]
    small_letters = [random.choice(string.letters.lower()) for _ in range(7)]
    p = numbers + big_letters + small_letters
    random.shuffle(p)
    return ''.join(p)

users = []

for idx in range(student_cnt):
    password = generate_pass()
    user = "student{}".format(idx + 1)
    out = subprocess.check_output(
        """
        az ad user create \
        --user-principal-name "{u}@zimovnovgmail.onmicrosoft.com" \
        --display-name "{u}" \
        --password {p} \
        --mail-nickname "{u}"
        """.format(p=password, u=user),
        shell=True
    )
    out = json.loads(out)
    userId = out["objectId"]
    users.append([user, password, userId])
    print user, "done"

df = pd.DataFrame(users, columns=["user", "password", "userId"])
df.to_json("users.json", orient="records")