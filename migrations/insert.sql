INSERT INTO public.users(
	username, email, password)
	VALUES (?, ?, ?);

INSERT INTO public.tasks(
	title, description, completed, created_at, updated_at, user_id)
	VALUES (?, ?, ?, ?, ?, ?);

INSERT INTO public.instagram(
	url, username, bio, followers, verified, task_id)
	VALUES (?, ?, ?, ?, ?, ?);

INSERT INTO public.facebook(
	url, username, bio, followers, verified, task_id)
	VALUES (?, ?, ?, ?, ?, ?);

INSERT INTO public.telegram(
	url, username, bio, followers, verified, task_id)
	VALUES (?, ?, ?, ?, ?, ?);