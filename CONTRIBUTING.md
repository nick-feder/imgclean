# contributing to imgclean

first off, thanks for taking the time to contribute! 

## how to contribute

### reporting bugs

found a bug? please open an issue with:
- clear description
- steps to reproduce  
- expected vs actual behavior
- your environment (os, python version)

### suggesting features

have an idea? open an issue with:
- use case description
- proposed solution
- any alternatives you considered

### code contributions

1. fork the repo
2. create a branch (`git checkout -b feature/cool-feature`)
3. make your changes
4. add tests if needed
5. make sure tests pass (`python -m unittest discover tests`)
6. commit (`git commit -m 'add cool feature'`)
7. push (`git push origin feature/cool-feature`)
8. open a pull request

## coding style

- keep it simple and readable
- comments only when necessary (code should be self-explanatory)
- use lowercase for comments, keep them casual
- follow existing patterns in the codebase
- use meaningful variable names

## testing

run tests before submitting:
```bash
python -m unittest discover tests
```

add tests for new features in `tests/` directory

## commit messages

- use present tense ("add feature" not "added feature")
- keep first line under 50 characters
- be descriptive but concise

good:
```
add size filtering option
```

less good:
```
updated code
```

## questions?

not sure about something? just ask! open an issue or discussion.

thanks for contributing! 🙏
