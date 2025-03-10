import { Link } from "react-router-dom";

const Button = ({ text, styling, url }) => {
  return (
    <>
      <Link className={`btn ${styling}`} to={url}>
        {text}
      </Link>
    </>
  );
};

export default Button;
