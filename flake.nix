{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {inherit system;};
        python = pkgs.python311;
        pythonPackages = python.pkgs;
      in {
        devShell = pkgs.mkShell {
          buildInputs = with pythonPackages; [
            matplotlib
            numpy
            pandas
          ];
        };
      }
    );
}
