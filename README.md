# interview-todo

## Assignment

Our new TODO tracker app is launching tomorrow, and we're finally going to be rich! We do still have a few minor things we need to address though before launch. Could you please:

1. Give a quick pass through it to make sure the current functionality is ready to ship.
1. Add the ability to re-order items in the todo list.
1. Add some simple search functionality, to help power users find their todos.

## Dev Setup

1. Create a python venv.
1. Activate the venv.
1. `pip install -r requirements.txt`
1. `python -m app.server`

## Notes

- Treat the code you write, within reason, as though it was production code that you were going to be responsible for in the future.
- This app is powered by SQLite. This obviously wouldn't cut it for a real app, but for the purposes of this assignment we don't expect you to use anything else.
- Please feel free to ask questions if any of the requirements are vague.

## Found issues

- [x] Frontend return 404 on styles.css => Fix added static/css/styles.css

- [x] Unsupported Media Type => likely issues with header

  - found that POST is sending `Content-Type: application/x-www-form-urlencoded` maybe this is unexpected by the flask application
  - found the method we reading from the JSON method, replaced with form instead

- [x] Achieved the reordering (time spent 1 hour)

  - There is a transaction so updates are atomic
  - Issues
    - Not really any use if this app is multi user as the frontend won't be accurate to the actual ordering in the DB
    - Could add frontend reordering and a save button that would then reflect actual user
    - UI still looks pretty janky

- [] Adding full text search (time spend 10 min)
  - Going to just do frontend search for now
  - Could also use full text search on the database side
