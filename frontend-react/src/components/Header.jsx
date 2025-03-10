import Button from "./Button";
import { Link } from "react-router-dom";
import { AuthContext } from "../AuthProvider";
import { useContext } from "react";

const Header = () => {
  const { isLoggedIn, setIsLoggedIn } = useContext(AuthContext);

  return (
    <>
      <nav className="navbar container pt-3 pb-3 align-items-start">
        <Link className="navbar-brand text-light" to="/">
          Stock Prediction Portal
        </Link>

        <div>
          {isLoggedIn ? (
            <button className="btn btn-danger">Logout</button>
          ) : (
            <>
              <Button text="Login" styling="btn-outline-info" url="/login" />
              &nbsp; &nbsp;
              <Button text="Register" styling="btn-info" url="/register" />
            </>
          )}
        </div>
      </nav>
    </>
  );
};

export default Header;
