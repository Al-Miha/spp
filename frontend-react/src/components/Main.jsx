import Button from "./Button";
import Footer from "./Footer";
import Header from "./Header";

const Main = () => {
  return (
    <>
      <div className="container">
        <div className="p-5 text-center rounded bg-light-dark">
          <h1 className="text-light">Stock Prediction Portal</h1>
          <p className="text-light lead">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Veritatis
            rem reiciendis sapiente, cum ad debitis consequuntur. Aspernatur,
            esse facilis velit commodi eum veniam eaque iure perspiciatis
            officiis, adipisci sunt ab amet ipsam, cupiditate in nihil tempore
            laboriosam autem optio placeat. Labore praesentium sunt a incidunt,
            maxime laudantium! Sapiente, eum voluptate.
          </p>
          <Button
            text="Explore Now"
            styling="btn-outline-info"
            url="/dashboard"
          />
        </div>
      </div>
    </>
  );
};

export default Main;
