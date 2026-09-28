package com.ruoyi.download.domain;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 资料下载管理对象 demo_download
 * 
 * @author ruoyi
 * @date 2026-06-25
 */
public class DemoDownload extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 文件ID */
    private Long downId;

    /** 标题 */
    @Excel(name = "标题")
    private String downTitle;

    /** 排序 */
    @Excel(name = "排序")
    private Long downSeq;

    /** 下载地址 */
    @Excel(name = "下载地址")
    private String downUrl;

    /** 状态 */
    @Excel(name = "状态")
    private String downStatus;

    /** 创建用户 */
    private Long createUserId;

    public void setDownId(Long downId) 
    {
        this.downId = downId;
    }

    public Long getDownId() 
    {
        return downId;
    }

    public void setDownTitle(String downTitle) 
    {
        this.downTitle = downTitle;
    }

    public String getDownTitle() 
    {
        return downTitle;
    }

    public void setDownSeq(Long downSeq) 
    {
        this.downSeq = downSeq;
    }

    public Long getDownSeq() 
    {
        return downSeq;
    }

    public void setDownUrl(String downUrl) 
    {
        this.downUrl = downUrl;
    }

    public String getDownUrl() 
    {
        return downUrl;
    }

    public void setDownStatus(String downStatus) 
    {
        this.downStatus = downStatus;
    }

    public String getDownStatus() 
    {
        return downStatus;
    }

    public void setCreateUserId(Long createUserId) 
    {
        this.createUserId = createUserId;
    }

    public Long getCreateUserId() 
    {
        return createUserId;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("downId", getDownId())
            .append("downTitle", getDownTitle())
            .append("downSeq", getDownSeq())
            .append("downUrl", getDownUrl())
            .append("downStatus", getDownStatus())
            .append("createUserId", getCreateUserId())
            .append("createTime", getCreateTime())
            .append("updateTime", getUpdateTime())
            .toString();
    }
}
