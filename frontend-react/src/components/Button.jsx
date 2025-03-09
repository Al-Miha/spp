const Button = ({ text, styling }) => {
  return (
    <>
      <a className={`btn ${styling}`} href="">
        {text}
      </a>
    </>
  );
};

export default Button;
