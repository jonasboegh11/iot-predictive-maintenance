const errorHandler = (err, req, res, next) => {
  console.error(err.stack);

  const statusCode = err.statusCode || 500;
  const message = err.message || "Noget gik galt på serveren";

  res.status(statusCode).json({
    error: {
      message: message,
      status: statusCode,
    },
  });
};

module.exports = errorHandler;