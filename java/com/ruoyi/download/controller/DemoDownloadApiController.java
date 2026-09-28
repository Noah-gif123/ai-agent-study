package com.ruoyi.download.controller;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.ruoyi.common.annotation.Anonymous;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.page.TableDataInfo;
import com.ruoyi.download.domain.DemoDownload;
import com.ruoyi.download.service.IDemoDownloadService;
import com.ruoyi.web.controller.common.Const;

@Anonymous
@RestController
@RequestMapping("/api/download")
public class DemoDownloadApiController extends BaseController{

    @Autowired
    private IDemoDownloadService demoDownloadService;

    @GetMapping("/list")
    public TableDataInfo list(DemoDownload demoDownload)
    {
        startPage();
        demoDownload.setDownStatus(Const.STATUS_NORMAL);
        List<DemoDownload> list = demoDownloadService.selectDemoDownloadList(demoDownload);
        return getDataTable(list);
    }
}