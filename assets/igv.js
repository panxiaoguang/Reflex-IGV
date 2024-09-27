import React, { useEffect, useRef } from "react";
import igv from "../node_modules/igv/dist/igv.esm.min.js";

const IgvComponent = ({ genome, locus, tracks, onTrackClick }) => {
  const igvContainerRef = useRef(null);
  const browserRef = useRef(null);

  useEffect(() => {
    const options = {
      genome,
      locus,
      tracks,
    };

    if (!browserRef.current) {
      igv.createBrowser(igvContainerRef.current, options).then((browser) => {
        browserRef.current = browser;
        if (onTrackClick) {
          browser.on("trackclick", (track, popoverData) => {
            const trackName = track.name;
            const trackValue = popoverData.map((data) => ({
              name: data.name,
              value: data.value,
            }));
            onTrackClick(trackName, trackValue);
          });
        }
      });
    }

    // 清理函数，在组件卸载时调用
    return () => {
      if (browserRef.current) {
        igv.removeAllBrowsers()
      }
    };
  }, []);

  useEffect(() => {
    if (browserRef.current) {
      browserRef.current.search(locus);
    }
  }, [locus]);

  return <div ref={igvContainerRef} />;
};

export default IgvComponent;
