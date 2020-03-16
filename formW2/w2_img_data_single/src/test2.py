def repeats( name):
    name = name.replace("&", "").replace("groups llg", "groups llc").replace("group llg", "group llc").replace("§",
                                                                                                               "")
    for x in range(1, len(name)):
        substring = name[:x]

        if substring * (len(name) // len(substring)) + (substring[:len(name) % len(substring)]) == name:
            return (substring)

    return (name)

print(repeats("1100 rush chapel road ne 1100 rush chapel road ne adairsville ga 30103 adairsville ga 30103"))