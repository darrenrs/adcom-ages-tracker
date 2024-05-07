import Link from "next/link";

export default function UserLogin() {
  return (
    <>
      <form className="flex flex-col items-center justify-center">
        <h1 className="global-title">Login</h1>
        <div className="m-4">
          <label htmlFor="username" className="block lg:text-lg">Username</label>
          <input type="text" id="username" name="username" className="user-form" />
        </div>
        <div className="m-4">
          <label htmlFor="password" className="block lg:text-lg">Password</label>
          <input type="password" id="password" name="password" className="user-form" />
        </div>
        <div className="m-4">
          <input type="button" value="Login" />
        </div>
        <div>
          <Link href="/user" className="global-link">Create Account</Link> • <Link href="/user" className="global-link">Forgot Password</Link>
        </div>
      </form>
    </>
  );
}
