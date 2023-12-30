{ pkgs ? import <nixpkgs> { } }:
let

  inherit (pkgs) stdenv lib fetchurl;

  sdk = stdenv.mkDerivation rec {
    pname = "TobiiPro-SDK-C";
    version = "1.11.0.1";

    src = fetchurl {
      url = "https://s3.eu-west-1.amazonaws.com/tobiipro.sdk/C/${version}/TobiiPro.SDK.C_Binding.LINUX_${version}.tar.gz";
      hash = "sha256-zbpBsxW24SV5bJgcMEVTXvT5WgyInuBb+Wvk92XXjBE=";
    };

    sourceRoot = ".";

    makeFlags = [
      "PREFIX=$(out)/"
    ];

    postPatch = ''
      substituteInPlace Makefile --replace "TSDK_NAME:=tobii_research" "TSDK_NAME:="
      substituteInPlace pkgconfig/tobii_research.pc --replace "/tobii_research" ""
      substituteInPlace pkgconfig/tobii_research.pc --replace "prefix=/usr/local" "prefix=$out"
    '';
  };

  libraryPath = with pkgs; lib.makeLibraryPath [
    avahi
    stdenv.cc.cc.lib
    sdk
  ];

in

pkgs.mkShell {
  LD_LIBRARY_PATH = libraryPath;
}
