const SimpleOracle = artifacts.require("SimpleOracle");

module.exports = function (deployer) {
  const initialValue = 42;  // example value i gave

  deployer.deploy(SimpleOracle, initialValue)  // Pass the initialValue for depolyment mitigation script
    .then(instance => {
      console.log("SimpleOracle deployed at:", instance.address);
    })
    .catch(err => {
      console.error("Error deploying SimpleOracle:", err);
    });
};
